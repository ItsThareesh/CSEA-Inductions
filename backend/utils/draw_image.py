import cv2
import numpy as np
from PIL import Image

def draw_score_on_image(image: Image.Image, score: float) -> Image.Image:
    """Draw the aesthetic score on the image."""
    # Convert PIL Image to OpenCV format
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Define font and scale
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 3
    color = (255, 255, 255)
    thickness = 5

    # Prepare the text
    text = f"Aesthetic Score: {score:.1f}"

    # Get text size
    (text_width, text_height), _ = cv2.getTextSize(text, font, scale, thickness)

    # Set position: bottom-left corner
    position = (10, cv_image.shape[0] - 10)

    # Draw rectangle background for better visibility
    cv2.rectangle(
        cv_image,
        (position[0] - 5, position[1] + 5),
        (position[0] + text_width + 5, position[1] - text_height - 5),
        (0, 0, 0),  # Black background
        -1
    )

    # Put the text on the image
    cv2.putText(cv_image, text, position, font, scale, color, thickness)

    # Convert back to PIL Image
    result_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))

    return result_image
