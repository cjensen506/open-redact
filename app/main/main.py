from fastapi import FastAPI, File, UploadFile, HTTPException, Response
from fastapi.responses import StreamingResponse
import io

app = FastAPI()


@app.post("/redact_pdf",
          response_class=Response,
          responses={
              # Manually specify a possible response with our custom media type.
              200: {
                  "content": {"application/pdf": {}}
              }
          })
async def create_upload_file(file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf"]:
        raise HTTPException(status_code=415, detail="Unsupported Media Type")
    contents = io.BytesIO(await file.read())

    response = StreamingResponse(iter(contents), media_type='application/pdf')
    response.headers["Content-Disposition"] = "attachment; filename=export.pdf"

    return response
