from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
import io
from aesthetic_predictor import AestheticPredictor
from llm_suggestion import SuggestionLLM

app = FastAPI(title="LAION Aesthetic Score API")

# Load predictor
predictor = AestheticPredictor(
    aesthetic_weights_path="aesthetic_linear_head_weight.pth",
    device="cpu"
)

# suggestions_llm = SuggestionLLM()

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

        return {
            "score": round(score, 2),
            # "suggestions": suggestions
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
