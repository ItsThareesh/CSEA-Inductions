from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io

import numpy as np
from aesthetic_predictor import AestheticPredictor
from utils.suggestions_generation import generate_suggestions

app = FastAPI(title="LAION Aesthetic Score API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load predictor
predictor = AestheticPredictor(
    aesthetic_weights_path="./linear_head_weight-b-16.pth",
    device="cpu"
)

@app.get("/")
async def root():
    return {"message": "LAION Aesthetic Score API is running."}

@app.post("/rate")
async def rate_image(file: UploadFile = File(...)):
    # Basic validation
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Read image
    image_bytes = await file.read()

    if (len(image_bytes) > 3 * 1024 * 1024):
        raise HTTPException(status_code=400, detail="Image size exceeds 3MB limit")

    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except:
        raise HTTPException(status_code=400, detail="Invalid image file")

    # Predict score
    score = predictor.predict(image)
    suggestions = generate_suggestions(score, np.array(image))

    return {
        "score": round(score, 2),
        "suggestions": suggestions,
    }
