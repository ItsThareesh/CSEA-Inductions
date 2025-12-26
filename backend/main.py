import io
import numpy as np
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from aesthetic_predictor import AestheticPredictor
from utils.draw_image import draw_score_on_image
from utils.suggestions_generation import generate_suggestions

app = FastAPI(title="LAION Aesthetic Score API")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load predictor
predictor = AestheticPredictor(
    aesthetic_weights_path="linear_head_weight-b-16.pth",
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

        if len(image_bytes) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="Image too large (max 8MB)"
            )

        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Predict score
        score = predictor.predict(image)

        if score > 5.5:
            score = min(score*1.1, 10)  # Slight boost for high scores
        
        suggestions = generate_suggestions(score, np.array(image))

        return {
            "score": round(score, 2),
            "suggestion": suggestions
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
async def get_saliency_map(file: UploadFile = File(...)):
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