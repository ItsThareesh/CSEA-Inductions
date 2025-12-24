export interface RatedImage {
    id: string;
    imageUrl: string;
    score: number;
    timestamp: number;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function rateImage(file: File): Promise<{ score: number }> {
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

function fileToBase64Thumbnail(file: File) {
    const img = new Image();
    const url = URL.createObjectURL(file);

    return new Promise((resolve) => {
        img.onload = () => {
            const canvas = document.createElement("canvas");
            const scale = Math.min(300 / img.width, 300 / img.height, 1);

            canvas.width = img.width * scale;
            canvas.height = img.height * scale;

            const ctx = canvas.getContext("2d")!;
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

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
