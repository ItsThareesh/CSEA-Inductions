import { Trophy, Star } from 'lucide-react';
import { Card, CardContent } from "@/components/ui/card"
import { cn } from "@/lib/utils"

interface ScoreCardProps {
    score: number | null;
    suggestion: string | null;
    loading?: boolean;
}

export default function ScoreCard({ score, suggestion, loading }: ScoreCardProps) {
    const getColor = (score: number): string => {
        if (score >= 7) return 'from-green-400 to-emerald-600';
        if (score >= 6) return 'from-blue-400 to-blue-600';
        if (score >= 5) return 'from-yellow-400 to-yellow-600';
        if (score >= 4) return 'from-orange-400 to-orange-600';
        return 'from-red-400 to-red-600';
    };

    if (loading) {
        return (
            <div className="w-full max-w-md mx-auto">
                <Card className="shadow-2xl border-none animate-pulse-soft">
                    <CardContent className="p-12 text-center">
                        <div className="animate-spin rounded-full h-24 w-24 border-b-4 border-primary mx-auto"></div>
                        <p className="mt-6 text-muted-foreground text-lg font-medium">Analyzing your masterpiece...</p>
                    </CardContent>
                </Card>
            </div>
        );
    }

    if (score === null) {
        return (
            <div className="w-full max-w-md mx-auto">
                <Card className="shadow-xl border-4 border-dashed border-muted hover:border-primary/50 transition-colors duration-300">
                    <CardContent className="p-12 text-center">
                        <Star className="w-24 h-24 mx-auto text-muted-foreground mb-4" />
                        <p className="text-muted-foreground text-xl font-medium">Upload an image to reveal its score</p>
                    </CardContent>
                </Card>
            </div>
        );
    }

    return (
        <div className="w-full max-w-md mx-auto animate-pop">
            <Card className={cn(
                "bg-gradient-to-br border-none shadow-2xl transform hover:scale-105 transition-transform duration-300 relative overflow-hidden",
                getColor(score)
            )}>
                <div className="absolute top-0 left-0 w-full h-full bg-white opacity-10 bg-grid-pattern"></div>
                <CardContent className="p-12 text-center relative z-10">
                    <Trophy className="w-16 h-16 mx-auto text-white mb-4 animate-float" />
                    <h2 className="text-white text-2xl font-bold mb-4 opacity-90">Aesthetic Score</h2>
                    <div className="text-8xl font-black text-white mb-4 drop-shadow-lg">
                        {score.toFixed(1)}
                    </div>
                    {suggestion && (
                        <div className="inline-block bg-white/20 backdrop-blur-md rounded-3xl px-6 py-2 text-white text-xl font-bold mb-2 border border-white/30">
                            {suggestion}
                        </div>
                    )}
                </CardContent>
            </Card>
        </div>
    );
}
