import numpy as np
from PIL import Image
from paddleocr import PaddleOCR

ocr = PaddleOCR(
    lang="en",
    use_textline_orientation=True,
    use_doc_orientation_classify=True,
)

def extract_text(image: Image.Image) -> str:
    img = np.array(image)
    results = ocr.predict(img)

    lines = []
    for res in results:
        lines.extend(res['rec_texts'])

    return "\n".join(lines)

if __name__ == "__main__":
    image = Image.open("images.png").convert("RGB")
    print(extract_text(image))