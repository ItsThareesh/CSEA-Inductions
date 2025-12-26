export interface RatedImage {
    id: string;
    imageUrl: string;
    score: number;
    timestamp: number;
}

const API_URL = process.env.NEXT_PUBLIC_BACKEND_URL!;

export async function rateImage(file: File): Promise<{
    score: number;
    suggestions: string[];
}> {
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(`${API_URL}/rate`, {
        method: "POST",
        body: formData,
    });

    if (!res.ok) {
        throw new Error("Failed to rate image");
    }

    return res.json();
}

export async function downloadScoredImage(file: File, score: number) {
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(`${API_URL}/download?score=${score}`, {
        method: "POST",
        body: formData,
    });

    if (!res.ok) {
        throw new Error("Failed to download scored image");
    }

    const blob = await res.blob();
    triggerDownload(blob, "image_with_score.png");
}

export async function downloadSaliencyMap(file: File) {
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(`${API_URL}/saliency-map`, {
        method: "POST",
        body: formData,
    });

    if (!res.ok) {
        throw new Error("Failed to download saliency map");
    }

    const blob = await res.blob();
    triggerDownload(blob, "saliency_map.png");
}

function triggerDownload(blob: Blob, filename: string) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
}