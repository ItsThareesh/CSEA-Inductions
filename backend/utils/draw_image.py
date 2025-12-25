import cv2
import numpy as np
from PIL import Image

def draw_score_on_image(image: Image.Image, score: float) -> Image.Image:
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    h, w = cv_image.shape[:2]

    font = cv2.FONT_HERSHEY_SIMPLEX

    # Adaptive scale
    scale = max(0.6, w / 800)
    thickness = max(1, int(scale * 2))

    text = f"Aesthetic Score: {score:.1f}/10"

    padding = int(scale * 12)

    (text_width, text_height), _ = cv2.getTextSize(
        text, font, scale, thickness
    )

    x = padding
    y = padding + text_height

    # Background rectangle
    cv2.rectangle(
        cv_image,
        (x - padding, y - text_height - padding),
        (x + text_width + padding, y + padding),
        (0, 0, 0),
        -1
    )

    # Text
    cv2.putText(cv_image, text, (x, y), font, scale, (255, 255, 255), thickness, cv2.LINE_AA)

    image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

    return Image.fromarray(image)
