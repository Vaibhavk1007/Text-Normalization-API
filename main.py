from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from PIL import Image
import io

from normalizer import text_normalizer_pipeline
from ocr_engine import ocr_image, ocr_pdf

app = FastAPI(title="Document Text Repair API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/normalize")
async def normalize(
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
):
    # ❌ invalid input
    if not text and not file:
        raise HTTPException(
            status_code=400,
            detail="Provide either text or an image/PDF file"
        )

    if text and file:
        raise HTTPException(
            status_code=400,
            detail="Provide only one input: text OR file"
        )

    try:
        # TEXT FLOW
        if text:
            raw_text = text
            input_type = "text"

        # FILE FLOW
        else:
            filename = file.filename.lower()
            content = await file.read()
            input_type = "file"

            if filename.endswith((".png", ".jpg", ".jpeg")):
                image = Image.open(io.BytesIO(content)).convert("RGB")
                raw_text = ocr_image(image)

            elif filename.endswith(".pdf"):
                raw_text = ocr_pdf(content)

            else:
                raise HTTPException(
                    status_code=400,
                    detail="Unsupported file type"
                )

        # 🔥 SAME CLEANUP PIPELINE
        normalized_text = text_normalizer_pipeline(raw_text)

        return {
            "input_type": input_type,
            "raw_text": raw_text,
            "normalized_text": normalized_text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
