'use client';

import { useState, useRef, useEffect } from 'react';
import { Download, Share2, ImageIcon, UploadCloud } from 'lucide-react';
import ScoreCard from '@/components/ScoreCard';
import History from '@/components/History';
import { rateImage, saveRating, getRatingHistory, type RatedImage } from '@/lib/api';

export default function Home() {
    const [selectedImage, setSelectedImage] = useState<string | null>(null);
    const [score, setScore] = useState<number | null>(null);
    const [loading, setLoading] = useState(false);
    const [history, setHistory] = useState<RatedImage[]>([]);
    const [suggestion, setSuggestion] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    useEffect(() => {
        setHistory(getRatingHistory());
    }, []);

    const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (!file) return;

        // Validate file type
        if (!file.type.startsWith('image/')) {
            setError('Please select an image file');
            return;
        }

        setError(null);

        const previewUrl = URL.createObjectURL(file);
        setSelectedImage(previewUrl);

        setScore(null);
        setSuggestion(null);

        // Rate the image
        setLoading(true);
        try {
            const result = await rateImage(file);
            setScore(result.score);
            setSuggestion(result.suggestion);

            console.log(result.score, result.suggestion);

            await saveRating(file, result.score);
            setHistory(getRatingHistory());
        } catch (err) {
            setError('Failed to rate image. Make sure the API server is running.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleUploadClick = () => {
        fileInputRef.current?.click();
    };

    const handleDownload = () => {
        return;
    };

    const handleShare = async () => {
        if (score === null) return;

        const shareData = {
            title: 'Aesthetic Score',
            text: `My image scored ${score.toFixed(1)}/10 on the aesthetic scale!`,
            url: window.location.href,
        };

        try {
            if (navigator.share) {
                await navigator.share(shareData);
            } else {
                // Fallback: copy to clipboard
                await navigator.clipboard.writeText(
                    `My image scored ${score.toFixed(1)}/10 on the aesthetic scale! Try it yourself at ${window.location.href}`
                );
                alert('Share text copied to clipboard!');
            }
        } catch (err) {
            console.error('Error sharing:', err);
        }
    };

    return (
        <main className="min-h-screen bg-gradient-to-br from-slate-50 via-slate-100 to-indigo-100 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950 py-12 px-4">
            <div className="max-w-6xl mx-auto">
                {/* Header */}
                <div className="text-center mb-12">
                    <h1 className="text-5xl md:text-6xl font-bold leading-snug text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-blue-600 mb-4">
                        Aesthetic Image Rater
                    </h1>
                    {/* <p className="text-xl text-gray-600 dark:text-gray-300">
                        Powered by LAION Aesthetic Predictor
                    </p> */}
                </div>

                {/* Main Content Area */}
                <div className="grid md:grid-cols-2 gap-8 mb-12">
                    {/* Upload Section */}
                    <div className="space-y-6">
                        <div
                            onClick={handleUploadClick}
                            className="relative bg-white dark:bg-gray-800 rounded-2xl shadow-xl overflow-hidden cursor-pointer hover:shadow-2xl transition-shadow duration-300 group"
                            style={{ minHeight: '400px' }}
                        >
                            {selectedImage ? (
                                <div className="relative w-full max-w-none aspect-[4/3] overflow-hidden group flex-shrink-0">
                                    <img
                                        src={selectedImage}
                                        alt="Selected"
                                        className="absolute inset-0 w-full h-full object-cover max-w-none"
                                    />

                                    <div className="absolute inset-0 bg-black/0 group-hover:bg-black/30 transition-colors duration-300 flex items-center justify-center">
                                        <div className="opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col items-center text-center">
                                            <UploadCloud className="w-16 h-16 text-white" />
                                            <p className="text-white text-lg font-semibold mt-2">
                                                Change Image
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            ) : (
                                <div className="flex flex-col items-center justify-center h-full min-h-[400px] p-12">
                                    <ImageIcon className="w-24 h-24 text-gray-300 dark:text-gray-600 mb-6" />
                                    <p className="text-2xl font-semibold text-gray-600 dark:text-gray-300 mb-2">
                                        Click to Upload
                                    </p>
                                    <p className="text-gray-400 dark:text-gray-500">
                                        or drag and drop your image here
                                    </p>
                                </div>
                            )}
                        </div>

                        <input
                            ref={fileInputRef}
                            type="file"
                            accept="image/*"
                            onChange={handleFileSelect}
                            className="hidden"
                        />

                        {/* Action Buttons */}
                        {score !== null && (
                            <div className="flex gap-4">
                                <button
                                    onClick={handleDownload}
                                    className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-4 px-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 flex items-center justify-center gap-2"
                                >
                                    <Download className="w-5 h-5" />
                                    Download
                                </button>
                                <button
                                    onClick={handleShare}
                                    className="flex-1 bg-purple-600 hover:bg-purple-700 text-white font-semibold py-4 px-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 flex items-center justify-center gap-2"
                                >
                                    <Share2 className="w-5 h-5" />
                                    Share
                                </button>
                            </div>
                        )}

                        {error && (
                            <div className="bg-red-100 dark:bg-red-900 border border-red-400 dark:border-red-700 text-red-700 dark:text-red-200 px-4 py-3 rounded-xl">
                                {error}
                            </div>
                        )}
                    </div>

                    {/* Score Section */}
                    <div className="flex items-center justify-center">
                        <ScoreCard score={score} suggestion={suggestion} loading={loading} />
                    </div>
                </div>

                {/* History Section */}
                <History history={history} />

                {/* Footer */}
                <div className="mt-16 text-center text-gray-500 dark:text-gray-400">
                    <p className="text-sm">
                        This tool uses the LAION Aesthetic Predictor to evaluate image quality.
                    </p>
                    <p className="text-xs mt-2">
                        Scores range from 1-10, with higher scores indicating better aesthetic quality.
                    </p>
                </div>
            </div>
        </main>
    );
}
