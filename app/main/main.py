from typing import List, Optional
from fastapi import FastAPI, File, Form, UploadFile, HTTPException, Response
from fastapi.responses import RedirectResponse
import io
import uvicorn
from app.main.pdf_processing import Redactor
from app.main.sensitive_text_check import supported_entities

app = FastAPI()


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.get("/entities")
async def list_entities():
    """List the PII entity types that can be requested for redaction."""
    return {"entities": sorted(supported_entities())}


def _parse_entities(entities: Optional[List[str]]) -> List[str]:
    """Normalize and validate the requested entity types.

    Accepts repeated form fields and/or comma-separated values, e.g.
    ``entities=PERSON&entities=EMAIL_ADDRESS`` or ``entities=PERSON,EMAIL_ADDRESS``.
    """
    parsed = []
    for raw in entities or []:
        parsed.extend(part.strip().upper() for part in raw.split(",") if part.strip())

    if not parsed:
        raise HTTPException(
            status_code=400,
            detail="At least one entity type must be specified. Send 'entities' as "
                   "multipart/form-data field(s) alongside the file (not as a URL "
                   "query parameter), e.g. -F \"entities=PERSON\" -F \"entities=EMAIL_ADDRESS\". "
                   "See GET /entities for the supported values.",
        )

    supported = set(supported_entities())
    invalid = [entity for entity in parsed if entity not in supported]
    if invalid:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Unsupported entity type(s).",
                "invalid": invalid,
                "supported": sorted(supported),
            },
        )

    return parsed


@app.post("/redact_pdf",
          response_class=Response,
          responses={
              # Manually specify a possible response with our custom media type.
              200: {
                  "content": {"application/pdf": {}}
              },
              400: {},
              415: {}
          })
async def create_upload_file(
    file: UploadFile = File(...),
    entities: Optional[List[str]] = Form(
        None,
        description="PII entity types to redact (e.g. PERSON, EMAIL_ADDRESS). "
                    "Repeat the field or use a comma-separated list. "
                    "See GET /entities for supported values.",
    ),
):
    if file.content_type not in ["application/pdf"]:
        raise HTTPException(status_code=415, detail="Unsupported Media Type")

    entities_to_redact = _parse_entities(entities)

    contents = io.BytesIO(await file.read())

    redactor = Redactor(contents, entities_to_redact)

    response = Response(content=redactor.redaction(), media_type="application/pdf")

    return response

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")
