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
            "Composition could be somewhat cluttered.",
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

def color_heuristics(image_bgr: np.ndarray) -> dict:
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    
    sat = hsv[..., 1] / 255.0 # just saturation channel normalized

    p25 = np.percentile(sat, 25)
    p75 = np.percentile(sat, 75)
    mean = sat.mean()
    std = sat.std()

    return {
        "low_color": p75 < 0.35,
        "high_color": p25 > 0.45,
        "washed_out": mean < 0.35 and std < 0.10,
        "oversaturated": mean > 0.60 and std < 0.12,
    }

def brightness_heuristic(image_bgr: np.ndarray) -> dict:
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    brightness = gray / 255.0

    p10 = np.percentile(gray, 10)
    p25 = np.percentile(gray, 25)
    p75 = np.percentile(gray, 75)
    p90 = np.percentile(gray, 90)

    mean = gray.mean()
    std = gray.std()

    return {
        # Overall exposure
        "underexposed": p75 < 0.35,
        "overexposed": p25 > 0.70,

        # Detail loss
        "shadow_crush": p10 < 0.05 and std < 0.15,
        "highlight_clipping": p90 > 0.95 and std < 0.15,

        # Flat lighting
        "low_contrast": std < 0.12,
    }

def interpret_heuristics(image_bgr: np.ndarray) -> dict:
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    brightness_flags = brightness_heuristic(image_bgr)
    saturation_flags = color_heuristics(image_bgr)
    
    return {
        **brightness_flags,
        **saturation_flags,
        "blurry": sharpness < 100,
        "very_sharp": sharpness > 300
    }
    
def heuristic_suggestions(flags: dict) -> list[str]:
    suggestion = {
        "underexposed": "The image appears underexposed. Try brighter lighting.",
        "overexposed": "Highlights are blown out. Reducing exposure may help.",
        "shadow_crush": "Details are lost in shadows. Increase fill light or exposure.",
        "highlight_clipping": "Details are lost in highlights. Lower exposure or use HDR.",
        "low_contrast": "The image looks flat. Increasing contrast can add depth.",
        "blurry": "The image looks slightly blurry. Improve focus or stability.",
        "low_color": "Colors appear muted. Increasing saturation could help.",
        "high_color": "Strong colors add impact, but be careful of oversaturation.",
        "washed_out": "Colors appear washed out. Increasing contrast or saturation may help.",
        "oversaturated": "Colors feel overly intense. Slight desaturation could improve balance.",
        "very_sharp": "The image is very sharp, which enhances detail and clarity.",
    }

    s = []

    for flag, active in flags.items():
        if active and flag in suggestion:
            s.append(suggestion[flag])

    return s

def generate_suggestions(score: float, image_bgr: np.ndarray) -> list[str]:
    flags = interpret_heuristics(image_bgr)

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
