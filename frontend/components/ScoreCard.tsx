import { Trophy, Star } from 'lucide-react';

interface ScoreCardProps {
    score: number | null;
    loading?: boolean;
}

export default function ScoreCard({ score, loading }: ScoreCardProps) {
    const getGrade = (score: number): string => {
        if (score >= 7) return 'Excellent';
        if (score >= 6) return 'Great';
        if (score >= 5) return 'Good';
        if (score >= 4) return 'Average';
        return 'Needs Work';
    };

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
                <div className="rounded-3xl shadow-2xl p-12 text-center animate-pulse-soft">
                    <div className="animate-spin rounded-full h-24 w-24 border-b-4 border-blue-500 mx-auto"></div>
                    <p className="mt-6 text-gray-600 dark:text-gray-300 text-lg font-medium">Analyzing your masterpiece...</p>
                </div>
            </div>
        );
    }

    if (score === null) {
        return (
            <div className="w-full max-w-md mx-auto">
                <div className="rounded-3xl shadow-xl p-12 text-center border-4 border-dashed border-gray-300 dark:border-gray-600 hover:border-blue-400 dark:hover:border-blue-500 transition-colors duration-300">
                    <Star className="w-24 h-24 mx-auto text-gray-300 dark:text-gray-600 mb-4" />
                    <p className="text-gray-600 dark:text-gray-400 text-xl font-medium">Upload an image to reveal its score</p>
                </div>
            </div>
        );
    }

    return (
        <div className="w-full max-w-md mx-auto animate-pop">
            <div className={`bg-gradient-to-br ${getColor(score)} rounded-3xl shadow-2xl p-12 text-center transform hover:scale-105 transition-transform duration-300 relative overflow-hidden`}>
                <div className="absolute top-0 left-0 w-full h-full bg-white opacity-10 bg-grid-pattern"></div>
                <div className="relative z-10">
                    <Trophy className="w-16 h-16 mx-auto text-white mb-4 animate-float" />
                    <h2 className="text-white text-2xl font-bold mb-4 opacity-90">Aesthetic Score</h2>
                    <div className="text-8xl font-black text-white mb-4 drop-shadow-lg">
                        {score.toFixed(1)}
                    </div>
                    <div className="inline-block bg-white/20 backdrop-blur-md rounded-full px-6 py-2 text-white text-2xl font-bold mb-2 border border-white/30">
                        {getGrade(score)}
                    </div>
                    <div className="text-white/80 text-sm font-medium mt-2">
                        out of 10.0
                    </div>
                </div>
            </div>
        </div>
    );
}
