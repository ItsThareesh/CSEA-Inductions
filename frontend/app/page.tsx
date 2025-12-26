'use client';

import { useState, useRef, useEffect } from 'react';
import { Download, ImageIcon, UploadCloud } from 'lucide-react';

import ScoreCard from '@/components/ScoreCard';
import History from '@/components/History';

import {
    rateImage,
    downloadScoredImage,
    downloadSaliencyMap,
    type RatedImage,
} from '@/lib/api';

import {
    fileToBase64Thumbnail,
    getRatingHistory,
    saveRating,
    getRatingObject,
} from '@/lib/helper';

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { ThemeToggle } from "@/components/theme-toggle";

export default function Home() {
    const fileInputRef = useRef<HTMLInputElement>(null);

    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [selectedImage, setSelectedImage] = useState<string | null>(null);

    const [score, setScore] = useState<number | null>(null);
    const [suggestion, setSuggestion] = useState<string[] | null>(null);

    const [history, setHistory] = useState<RatedImage[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Load history on mount
    useEffect(() => {
        const loadHistory = async () => {
            const history = await getRatingHistory();
            setHistory(history);
        };

        loadHistory();
    }, []);

    // Clean up object URL on unmount
    useEffect(() => {
        return () => {
            if (selectedImage) {
                URL.revokeObjectURL(selectedImage);
            }
        };
    }, [selectedImage]);

    const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (!file) return;

        // Validate
        if (!file.type.startsWith('image/')) {
            setError('Please select an image file');
            return;
        }

        if (file.size > 3 * 1024 * 1024) {
            setError('Please select an image smaller than 3MB');
            return;
        }

        setError(null);
        setLoading(true);

        setSelectedFile(file);
        setSelectedImage(URL.createObjectURL(file));
        setScore(null);
        setSuggestion(null);

        try {
            // Rate Image
            const result = await rateImage(file);
            setScore(result.score);
            setSuggestion(result.suggestions);

            // Create Thumbnail
            const thumbnail = await fileToBase64Thumbnail(file);

            // Check Duplicates
            const existingHistory = await getRatingHistory();
            const exists = existingHistory.some(
                item =>
                    item.imageUrl === thumbnail &&
                    Math.abs(item.score - result.score) < 0.01
            );

            if (!exists) {
                const ratingObject = await getRatingObject(result.score, thumbnail);
                const updated = await saveRating(ratingObject);
                setHistory(updated);
            }
        } catch (err) {
            console.error(err);
            setError('Failed to rate image. Make sure the API server is running.');
        } finally {
            setLoading(false);
        }
    };

    const handleUploadClick = () => {
        fileInputRef.current?.click();
    };

    return (
        <main className="min-h-screen bg-background py-12 px-4 relative">
            <ThemeToggle />

            <div className="max-w-6xl mx-auto">
                {/* Header */}
                <div className="text-center mb-12">
                    <h1 className="text-5xl md:text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-primary via-blue-500 to-cyan-400 mb-4 pb-2">
                        Aesthetic Image Rater
                    </h1>
                </div>

                {/* Main grid */}
                <div className="grid md:grid-cols-2 gap-8 mb-12">

                    {/* Upload */}
                    <div className="space-y-6">
                        <Card
                            onClick={handleUploadClick}
                            className={cn(
                                "relative overflow-hidden cursor-pointer transition-all group border-2 border-dashed border-muted-foreground/25 hover:border-primary/50",
                                selectedImage && "border-none"
                            )}
                        >
                            <CardContent className="p-0 min-h-[400px] flex items-center justify-center">
                                {selectedImage ? (
                                    <div className="relative w-full h-full aspect-[4/3]">
                                        <img
                                            src={selectedImage}
                                            alt="Selected"
                                            className="w-full h-full object-cover"
                                        />
                                        <div className="absolute inset-0 bg-black/0 group-hover:bg-black/30 transition-colors flex items-center justify-center">
                                            <div className="opacity-0 group-hover:opacity-100 transition-opacity flex flex-col items-center text-center">
                                                <UploadCloud className="w-16 h-16 text-white" />
                                                <p className="text-white text-lg font-semibold mt-2">
                                                    Change Image
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                ) : (
                                    <div className="flex flex-col items-center justify-center p-12 text-center">
                                        <div className="bg-muted rounded-full p-6 mb-6">
                                            <ImageIcon className="w-12 h-12 text-muted-foreground" />
                                        </div>
                                        <p className="text-2xl font-semibold text-muted-foreground">
                                            Click to Upload
                                        </p>
                                    </div>
                                )}
                            </CardContent>
                        </Card>

                        <input
                            ref={fileInputRef}
                            type="file"
                            accept="image/*"
                            onChange={handleFileSelect}
                            className="hidden"
                        />

                        {/* Actions */}
                        {score !== null && selectedFile && (
                            <div className="flex gap-4">
                                <Button
                                    onClick={() => downloadScoredImage(selectedFile, score)}
                                    className="flex-1 h-14 text-lg"
                                >
                                    <Download className="w-5 h-5 mr-2" />
                                    Download Score
                                </Button>

                                <Button
                                    onClick={() => downloadSaliencyMap(selectedFile)}
                                    variant="secondary"
                                    className="flex-1 h-14 text-lg"
                                >
                                    <Download className="w-5 h-5 mr-2" />
                                    Download Attention Map
                                </Button>
                            </div>
                        )}

                        {error && (
                            <div className="bg-destructive/10 border border-destructive/20 text-destructive px-4 py-3 rounded-xl">
                                {error}
                            </div>
                        )}
                    </div>

                    {/* Score */}
                    <div className="flex items-center justify-center">
                        <ScoreCard
                            score={score}
                            suggestion={suggestion}
                            loading={loading}
                        />
                    </div>
                </div>

                {/* History */}
                <History history={history} />

                {/* Footer */}
                <div className="mt-16 text-center text-muted-foreground">
                    <p className="text-sm">
                        Uses the LAION Aesthetic Predictor for image quality evaluation.
                    </p>
                    <p className="text-xs mt-2">
                        Scores range from 1-10.
                    </p>
                </div>
            </div>
        </main>
    );
}