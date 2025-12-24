import io
from PIL import Image
from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel
from clip import ClipSimilarity
from ocr import extract_text
from vibe_classifier import detect_vibe

app = FastAPI()

DEFAULT_MEME_TEMPLATES = [
    # Distracted Boyfriend
    "a man looking at another woman while his girlfriend looks angry meme",

    # Drake Hotline Bling
    "a man rejecting something in the top panel and approving something in the bottom panel meme",

    # Two Buttons
    "a cartoon hand hovering over two red buttons decision meme",

    # Expanding Brain
    "a series of images showing an expanding glowing brain stages meme",

    # Change My Mind
    "a man sitting at a table with a sign that says change my mind meme",

    # Is This a Pigeon
    "a man pointing at a butterfly and asking is this a pigeon meme",

    # Woman Yelling at a Cat
    "a woman yelling angrily and a confused cat sitting at a dinner table meme",

    # Surprised Pikachu
    "a surprised pikachu face reaction meme",

    # Mocking SpongeBob
    "a spongebob character mocking with bent arms chicken pose meme",

    # One Does Not Simply
    "a man saying one does not simply walk into mordor meme",

    # Batman Slapping Robin
    "a comic panel where batman slaps robin meme",

    # This Is Fine
    "a cartoon dog sitting calmly in a burning room meme",

    # Gru's Plan
    "a man presenting a plan on a board that fails step by step meme",

    # Left Exit 12 Off Ramp
    "a highway sign showing a car dangerously taking a sudden exit meme",

    # Waiting Skeleton
    "a skeleton sitting and waiting patiently meme",

    # Disaster Girl
    "a little girl smiling in front of a burning house meme",

    # Ancient Aliens
    "a man with wild hair explaining something with aliens meme",

    # UNO Draw 25
    "uno draw 25 card decision meme",

    # Trade Offer
    "a trade offer meme showing i receive and you receive text",

    # Boardroom Meeting
    "people in a business meeting pointing and arguing meme"
]

clip = ClipSimilarity()
clip.compute_text_embeddings(DEFAULT_MEME_TEMPLATES)

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

    scores = clip.compute_similarity(image)
    best_idx = max(range(len(scores)), key=lambda i: scores[i])
    best_score = scores[best_idx]
    best_template = DEFAULT_MEME_TEMPLATES[best_idx]

    CONFIDENCE_THRESHOLD = 0.22

    if best_score < CONFIDENCE_THRESHOLD:
        template = "unknown"
    else:
        template = best_template
    
    return {
        "extracted_text": text,
        "meme_template": template
    }

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
