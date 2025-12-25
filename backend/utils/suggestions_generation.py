import random
import cv2
import numpy as np

def score_bucket(score: float) -> str:
    SUGGESTIONS = {
        "excellent": [
            "Strong composition and visual clarity.",
            "Lighting enhances the subject effectively.",
            "The image feels intentional and polished."
        ],
        "good": [
            "Good overall composition.",
            "The subject is clear, but could stand out more.",
            "Minor adjustments could elevate the image."
        ],
        "average": [
            "The image lacks a strong focal point.",
            "Lighting could be improved for clarity.",
            "Simplifying the scene may help."
        ],
        "poor": [
            "The subject is difficult to identify.",
            "Lighting issues reduce visual impact.",
            "Reframing the shot could help significantly."
        ],
    }

    if score >= 8:
        return SUGGESTIONS["excellent"]
    elif score >= 6:
        return SUGGESTIONS["good"]
    elif score >= 4:
        return SUGGESTIONS["average"]
    
    return SUGGESTIONS["poor"]

def extract_heuristics(image_bgr: np.ndarray) -> dict:
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    brightness = gray.mean() / 255.0
    sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
    saturation = hsv[..., 1].mean()

    return {
        "brightness": brightness,
        "sharpness": sharpness,
        "saturation": saturation,
    }


def interpret_heuristics(h: dict) -> dict:
    return {
        "underexposed": h["brightness"] < 0.35,
        "overexposed": h["brightness"] > 0.75,
        "blurry": h["sharpness"] < 100,
        "very_sharp": h["sharpness"] > 300,
        "low_color": h["saturation"] < 0.25,
        "high_color": h["saturation"] > 0.7,
    }
    
def heuristic_suggestions(flags: dict) -> list[str]:
    s = []

    if flags["underexposed"]:
        s.append("The image appears underexposed. Try brighter lighting.")
    if flags["overexposed"]:
        s.append("Highlights are blown out. Reducing exposure may help.")
    if flags["blurry"]:
        s.append("The image looks slightly blurry. Improve focus or stability.")
    if flags["low_color"]:
        s.append("Colors appear muted. Increasing saturation could help.")
    if flags["high_color"]:
        s.append("Strong colors add impact, but be careful of oversaturation.")

    return s

def generate_suggestions(score: float, image_bgr: np.ndarray) -> list[str]:
    heuristics = extract_heuristics(image_bgr)
    flags = interpret_heuristics(heuristics)

    heuristic_msgs = heuristic_suggestions(flags)
    bucket_msgs = score_bucket(score)

    final = []

    # Heuristic-based suggestions come first first
    final.extend(random.sample(heuristic_msgs, min(2, len(heuristic_msgs))))

    # Fill remaining slots with bucket-based
    remaining = 3 - len(final)
    if remaining > 0:
        final.extend(random.sample(bucket_msgs, min(remaining, len(bucket_msgs))))

    return final
