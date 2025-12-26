"use server"

export interface RatedImage {
    id: string;
    imageUrl: string;
    score: number;
    timestamp: number;
}

const API_URL = process.env.INTERNAL_BACKEND_URL;

export async function rateImage(file: File): Promise<{ score: number, suggestions: string[] }> {
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

    const response = await fetch(`${API_URL}/download?score=${score}`, {
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
