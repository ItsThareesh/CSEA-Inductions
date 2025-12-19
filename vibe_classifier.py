from transformers import pipeline

emotion_classifier = pipeline(
    task="text-classification",
    model="SamLowe/roberta-base-go_emotions",
    return_all_scores=True
)

EMOTION_TO_VIBE = {
    # wholesome
    "admiration": "wholesome",
    "gratitude": "wholesome",
    "joy": "wholesome",
    "love": "wholesome",
    "caring": "wholesome",
    "pride": "wholesome",
    "relief": "wholesome",

    # sarcastic
    "amusement": "sarcastic",
    "optimism": "sarcastic",
    "confusion": "sarcastic",
    "realization": "sarcastic",
    "curiosity": "sarcastic",
    "surprise": "sarcastic",
    "excitement": "sarcastic",

    # rage
    "anger": "rage",
    "annoyance": "rage",
    "disapproval": "rage",

    # cringe
    "disgust": "cringe",
    "embarrassment": "cringe",
    "remorse": "cringe",

    # neutral
    "neutral": "neutral",
    "sadness": "neutral",
    "fear": "neutral",
    "nervousness": "neutral",
    "disappointment": "neutral",
    "grief": "neutral",
    "desire": "neutral",
    "approval": "neutral",
}

def detect_vibe(text: str):
    results = emotion_classifier(text)[0]

    # pick strongest emotion
    top = max(results, key=lambda x: x["score"])
    emotion = top["label"]
    score = round(top["score"], 3)

    if score < 0.4:
        emotion = "neutral"

    vibe = EMOTION_TO_VIBE.get(emotion)

    return {
        "vibe": vibe,
        "tags": [emotion],
        "vibe_score": score
    }

if __name__ == "__main__":
    sample_text = "I absolutely love the way you handled that situation!"
    result = detect_vibe(sample_text)
    print(result)
