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

function fileToBase64(file: File) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

export async function saveRating(file: File, score: number) {
    const base64 = await fileToBase64(file);
    const history = getRatingHistory();

    // Avoid duplicates
    for (let item of history) {
        if (item.imageUrl === base64) {
            return;
        }
    }

    const newRating: RatedImage = {
        id: Date.now().toString(),
        imageUrl: base64 as string,
        score,
        timestamp: Date.now(),
    };

    const updatedHistory = [newRating, ...history].slice(0, 10);
    localStorage.setItem('ratingHistory', JSON.stringify(updatedHistory));
}

export function getRatingHistory(): RatedImage[] {
    if (typeof window === 'undefined') return [];

    const stored = localStorage.getItem('ratingHistory');

    console.log(stored);

    return stored ? JSON.parse(stored) : [];
}
