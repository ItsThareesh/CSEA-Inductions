import { RatedImage } from "./api";

export async function fileToBase64Thumbnail(file: File): Promise<string> {
    const img = new Image();
    const url = URL.createObjectURL(file);
    const dpr = window.devicePixelRatio || 1;

    return new Promise((resolve) => {
        img.onload = () => {
            const scale = Math.min(300 / img.width, 300 / img.height, 1);

            const targetWidth = Math.round(img.width * scale);
            const targetHeight = Math.round(img.height * scale);

            const canvas = document.createElement("canvas");
            canvas.width = targetWidth * dpr;
            canvas.height = targetHeight * dpr;

            const ctx = canvas.getContext("2d")!;
            ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

            ctx.imageSmoothingEnabled = true;
            ctx.imageSmoothingQuality = "high";

            ctx.drawImage(img, 0, 0, targetWidth, targetHeight);

            URL.revokeObjectURL(url);
            resolve(canvas.toDataURL("image/jpeg"));
        };

        img.src = url;
    });
}

export async function getRatingHistory(): Promise<RatedImage[]> {
    const stored = localStorage.getItem('ratingHistory');

    return stored ? JSON.parse(stored) : [];
}

export async function getRatingObject(score: number, base64thumb: string): Promise<RatedImage> {
    const newRating: RatedImage = {
        id: Date.now().toString(),
        imageUrl: base64thumb as string,
        score,
        timestamp: Date.now(),
    };

    return newRating;
}


export async function saveRating(rating: RatedImage) {
    const history = await getRatingHistory();
    const updated = [rating, ...history].slice(0, 10);

    localStorage.setItem("ratingHistory", JSON.stringify(updated));
    return updated;
}