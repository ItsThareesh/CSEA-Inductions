import random
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
from aesthetic_predictor import AestheticPredictor

app = FastAPI(title="LAION Aesthetic Score API")

# Enable CORS for the Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load predictor
predictor = AestheticPredictor(
    aesthetic_weights_path="aesthetic_linear_head_weight.pth",
    device="cpu"
)

@app.post("/rate")
async def rate_image(file: UploadFile = File(...)):
    # Basic validation
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Read image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Predict score
        score = predictor.predict(image)
        predictor.saliency_map(image)

        if score > 5.5:
            score *= 1.1  # Slight boost for high scores
            suggestions = [
                "Great composition!", "Vibrant colors!", "Well focused!",
                "Excellent lighting!", "Strong subject!", "Good use of depth!"

            ]
        else:
            suggestions = [
                "Needs work", "Improve lighting.", "Enhance composition.", "Increase sharpness.",
                "Adjust color balance.", "Consider cropping."
            ]

        return {
            "score": round(score, 2),
            "suggestion": suggestions[random.randint(0, len(suggestions)-1)]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
