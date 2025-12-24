import { RatedImage } from '@/lib/api';
import Image from 'next/image';

interface HistoryProps {
    history: RatedImage[];
}

export default function History({ history }: HistoryProps) {
    if (history.length === 0) {
        return (
            <div className="mt-12">
                <h3 className="text-2xl font-bold text-gray-800 dark:text-white mb-6 text-center">
                    Recent Ratings
                </h3>
                <p className="text-center text-gray-500 dark:text-gray-400">
                    No ratings yet. Upload your first image!
                </p>
            </div>
        );
    }

    return (
        <div className="mt-16">
            <h3 className="text-3xl font-bold text-gray-800 dark:text-white mb-8 text-center flex items-center justify-center gap-3">
                <span className="text-2xl">📜</span> Recent Ratings
            </h3>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-6">
                {history.map((item, index) => (
                    <div
                        key={item.id}
                        className="relative group overflow-hidden rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2"
                        style={{ animationDelay: `${index * 100}ms` }}
                    >
                        <div className="aspect-square relative bg-gray-200 dark:bg-gray-700">
                            <img
                                src={item.imageUrl}
                                alt="Rated image"
                                className="object-cover w-full h-full transition-transform duration-500 group-hover:scale-110"
                            />
                        </div>
                        <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-4">
                            <div className="transform translate-y-4 group-hover:translate-y-0 transition-transform duration-300">
                                <div className="text-white font-bold text-2xl mb-1">
                                    {item.score.toFixed(1)}
                                </div>
                                <div className="text-white/80 text-xs font-medium">
                                    {new Date(item.timestamp).toLocaleDateString()}
                                </div>
                            </div>
                        </div>
                        <div className={`absolute top-3 right-3 px-3 py-1 rounded-full text-sm font-bold text-white shadow-lg backdrop-blur-md
                            ${item.score >= 7 ? 'bg-green-500/80' :
                                item.score >= 5 ? 'bg-yellow-500/80' : 'bg-red-500/80'}`}>
                            {item.score.toFixed(1)}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
