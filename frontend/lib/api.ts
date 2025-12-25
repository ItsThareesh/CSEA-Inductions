export interface RatedImage {
    id: string;
    imageUrl: string;
    score: number;
    timestamp: number;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function rateImage(file: File): Promise<{ score: number, suggestion: string }> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_URL}/rate`, {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        throw new Error('Failed to rate image');
    }

    return response.json();
}

export async function downloadScoredImage(file: File, score: number) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('score', `${score}`);

    const response = await fetch(`${API_URL}/download`, {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        throw new Error("Failed to download scored image");
    }

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "image_with_score.png";
    document.body.appendChild(a);
    a.click();

    a.remove();
    URL.revokeObjectURL(url);
}

export async function downloadSaliencyMap(file: File) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_URL}/saliency-map`, {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        throw new Error("Failed to download saliency map");
    }

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "saliency_map.png";
    document.body.appendChild(a);
    a.click();

    a.remove();
    URL.revokeObjectURL(url);
}

function fileToBase64Thumbnail(file: File) {
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

export async function saveRating(file: File, score: number) {
    const base64thumb = await fileToBase64Thumbnail(file);
    const history = getRatingHistory();

    // Avoid duplicates
    for (let item of history) {
        if (item.imageUrl === base64thumb) {
            return;
        }
    }

    const newRating: RatedImage = {
        id: Date.now().toString(),
        imageUrl: base64thumb as string,
        score,
        timestamp: Date.now(),
    };

    const updatedHistory = [newRating, ...history].slice(0, 10);
    localStorage.setItem('ratingHistory', JSON.stringify(updatedHistory));
}

export function getRatingHistory(): RatedImage[] {
    if (typeof window === 'undefined') return [];

    const stored = localStorage.getItem('ratingHistory');

    return stored ? JSON.parse(stored) : [];
}
