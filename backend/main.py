import numpy as np
import io
from aesthetic_predictor import AestheticPredictor
from utils.draw_image import draw_score_on_image
from utils.suggestions_generation import generate_suggestions
from typing import Optional
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

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

@app.post("/download")
async def download_scored_image(
    file: UploadFile = File(...),
    score: Optional[float] = None
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Read image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # Annotate image with score if available
        if score is not None:
            annotated_image = draw_score_on_image(image, score)
        else:
            annotated_image = image
        
        # Convert annotated image to bytes
        buf = io.BytesIO()
        annotated_image.save(buf, format='PNG')
        buf.seek(0)

        return StreamingResponse(
            buf,
            media_type="image/png",
            headers={
                "Content-Disposition": "attachment; filename=annotated_image.png"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/saliency-map")
async def download_saliency_map(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Read image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Generate saliency map
        saliency_map = predictor.saliency_map(image)

        # Convert saliency map to bytes
        buf = io.BytesIO()
        saliency_map.save(buf, format='PNG')
        buf.seek(0)

        return StreamingResponse(
            buf,
            media_type="image/png",
            headers={
                "Content-Disposition": "attachment; filename=saliency_map.png"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))