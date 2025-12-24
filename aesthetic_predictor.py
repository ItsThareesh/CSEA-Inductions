import torch
import clip
from PIL import Image
from typing import Union


class AestheticPredictor(torch.nn.Module):
    """
    LAION Aesthetic Predictor with Linear Head
    """

    def __init__(
        self,
        aesthetic_weights_path: str,
        device: str | None = None,
    ):
        super().__init__()

        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        # Load CLIP
        self.clip_model, self.preprocess = clip.load(
            "ViT-B/32", device=self.device
        )
        self.clip_model.eval()

        # Aesthetic linear head (512 -> 1)
        self.aesthetic_head = torch.nn.Linear(512, 1)
        self.aesthetic_head.load_state_dict(
            torch.load(aesthetic_weights_path, map_location=self.device)
        )
        self.aesthetic_head.eval()
        self.aesthetic_head.to(self.device)

    @torch.no_grad()
    def predict(
        self,
        image: Union[str, Image.Image],
        normalize: bool = True,
    ) -> float:
        """
        Predict aesthetic score for an image.

        Args:
            image: Path to image or PIL Image
            normalize: Whether to normalize score to 0-10

        Returns:
            Aesthetic score (float)
        """

        # Load image
        if isinstance(image, str):
            image = Image.open(image).convert("RGB")
        elif not isinstance(image, Image.Image):
            raise ValueError("image must be a file path or PIL.Image")

        # Preprocess
        image_tensor = (
            self.preprocess(image)
            .unsqueeze(0)
            .to(self.device)
        )

        # CLIP embedding
        embedding = self.clip_model.encode_image(image_tensor)
        embedding = embedding / embedding.norm(dim=-1, keepdim=True)
        embedding = embedding.float()

        # Raw aesthetic score
        raw_score = self.aesthetic_head(embedding).item()

        if not normalize:
            return raw_score

        # Normalize to 0–10 (standard LAION scaling)
        score_0_10 = (raw_score - 1.0) * (10.0 / 8.0)

        return float(score_0_10)
