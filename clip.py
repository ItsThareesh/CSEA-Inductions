import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

class ClipSimilarity:
    def __init__(self, model_name="openai/clip-vit-large-patch14"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model = CLIPModel.from_pretrained(model_name).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(model_name)

        self.model.eval()
        self.text_embeddings = None

    @torch.no_grad()
    def compute_text_embeddings(self, texts: list[str]):
        inputs = self.processor(
            text=texts,
            return_tensors="pt",
            padding=True
        ).to(self.device)

        text_embeds = self.model.get_text_features(**inputs)
        text_embeds = text_embeds / text_embeds.norm(dim=-1, keepdim=True)

        self.text_embeddings = text_embeds
        return text_embeds.cpu()

    @torch.no_grad()
    def compute_similarity(self, image: Image.Image):
        if self.text_embeddings is None:
            raise ValueError("Call compute_text_embeddings() first")

        inputs = self.processor(
            images=image,
            return_tensors="pt"
        ).to(self.device)

        image_embed = self.model.get_image_features(**inputs)
        image_embed = image_embed / image_embed.norm(dim=-1, keepdim=True)

        similarity = image_embed @ self.text_embeddings.T
        return similarity.squeeze(0).cpu().tolist()