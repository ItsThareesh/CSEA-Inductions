import io
from PIL import Image
from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel
from ocr import extract_text
from vibe_classifier import detect_vibe

app = FastAPI()

@app.get("/")
async def read_root():
    return {"ok": True}

@app.post("/meme-read")
async def read_meme(
    file: UploadFile = File(...),
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    image_data = await file.read()

    try:
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")
    
    text = extract_text(image)
    
    return {"extracted_text": text}

class MemeEmotionRequest(BaseModel):
    text: str

class MemeEmotionResponse(BaseModel):
    sentiment: str
    tags: list[str]
    vibe_score: float

@app.post("/meme-emotion")
async def read_emotion(request: MemeEmotionRequest):
    text = request.text.strip()

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty"
        )

    result = detect_vibe(text)

    return result
