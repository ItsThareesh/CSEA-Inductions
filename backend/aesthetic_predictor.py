import os
import cv2
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

        return float(raw_score)

    def saliency_map(self, image, n_samples=24, noise_std=0.1):
        if isinstance(image, str):
            image = Image.open(image).convert("RGB")

        base = self.preprocess(image).unsqueeze(0).to(self.device)
        saliency_acc = torch.zeros_like(base)

        for _ in range(n_samples):
            noise = torch.randn_like(base) * noise_std
            noisy = (base + noise).clamp(0, 1)
            noisy.requires_grad_(True)

            embedding = self.clip_model.encode_image(noisy)
            embedding = embedding / embedding.norm(dim=-1, keepdim=True)
            embedding = embedding.float()

            score = self.aesthetic_head(embedding)
            score.backward()

            saliency_acc += noisy.grad.abs()
            self.clip_model.zero_grad()
            self.aesthetic_head.zero_grad()

        # Average gradients across samples and channels
        saliency = saliency_acc.mean(dim=0).mean(dim=0)

        # Normalize
        saliency = (saliency - saliency.min()) / (saliency.max() - saliency.min() + 1e-8)
        saliency = saliency.cpu().numpy()

        # Spatial smoothing
        saliency = cv2.GaussianBlur(saliency, (31, 31), 0)
        saliency = (saliency * 255).astype("uint8")

        # Create heatmap (BGR)
        heatmap = cv2.applyColorMap(saliency, cv2.COLORMAP_TURBO)
        heatmap = cv2.resize(heatmap, image.size)

        # Convert back to RGB for PIL
        saliency_image = Image.fromarray(cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB))

        # Ensure directory exists
        os.makedirs("saliency", exist_ok=True)
        saliency_image.save("saliency/saliency_map.png")

        return saliency_image
