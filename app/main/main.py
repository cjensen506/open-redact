from fastapi import FastAPI, File, UploadFile, HTTPException, Response
import io
from app.main.pdf_processing import Redactor

app = FastAPI()


@app.post("/redact_pdf",
          response_class=Response,
          responses={
              # Manually specify a possible response with our custom media type.
              200: {
                  "content": {"application/pdf": {}}
              },
              415: {}
          })
async def create_upload_file(file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf"]:
        raise HTTPException(status_code=415, detail="Unsupported Media Type")
    contents = io.BytesIO(await file.read())

    redactor = Redactor(contents)

    response = Response(content=redactor.redaction(), media_type="application/pdf")

    return response
