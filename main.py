from fastapi import FastAPI
from pydantic import BaseModel
from normalizer import text_normalizer_pipeline

app = FastAPI(
    title="Formyxa Text Normalizer API",
    version="1.0"
)

class NormalizeRequest(BaseModel):
    text: str

class NormalizeResponse(BaseModel):
    normalized_text: str

@app.post("/normalize", response_model=NormalizeResponse)
def normalize_text(payload: NormalizeRequest):
    output = text_normalizer_pipeline(payload.text)
    return {"normalized_text": output}