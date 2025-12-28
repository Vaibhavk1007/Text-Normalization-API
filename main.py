from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# import your pipeline function
from normalizer import text_normalizer_pipeline  # adjust filename if needed

app = FastAPI(title="Text Normalizer API")

# ✅ VERY IMPORTANT (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # later restrict to formyxa.com
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NormalizeRequest(BaseModel):
    text: str

class NormalizeResponse(BaseModel):
    normalized_text: str

@app.post("/normalize", response_model=NormalizeResponse)
def normalize_text(payload: NormalizeRequest):
    result = text_normalizer_pipeline(payload.text)
    return {"normalized_text": result}
