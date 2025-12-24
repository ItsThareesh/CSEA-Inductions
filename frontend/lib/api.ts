export interface RatedImage {
    id: string;
    imageUrl: string;
    score: number;
    timestamp: number;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

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

export function saveRating(imageUrl: string, score: number): void {
    const history = getRatingHistory();
    const newRating: RatedImage = {
        id: Date.now().toString(),
        imageUrl,
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
