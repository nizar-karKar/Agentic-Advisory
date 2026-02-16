import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { ChevronDown, ChevronUp, AlertCircle, CheckCircle, Lightbulb, TrendingUp } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const ArticleDisplay = ({ article, critique }) => {
    const [showCritique, setShowCritique] = useState(false);

    if (!article) return null;

    const renderCritiqueContent = () => {
        if (typeof critique === 'object') {
            return (
                <div className="space-y-4">
                    {Object.entries(critique).map(([key, value], index) => (
                        <motion.div
                            key={key}
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: index * 0.1 }}
                            className="bg-white/60 backdrop-blur-sm rounded-xl p-5 border border-indigo-100 shadow-sm hover:shadow-md transition-shadow"
                        >
                            <h5 className="font-bold text-gray-800 mb-2 capitalize flex items-center gap-2">
                                <div className="w-2 h-2 bg-indigo-500 rounded-full"></div>
                                {key.replace(/_/g, ' ')}
                            </h5>
                            <p className="text-gray-700 leading-relaxed">{String(value)}</p>
                        </motion.div>
                    ))}
                </div>
            );
        }
        return <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">{critique}</p>;
    };

    return (
        <div className="article-container">
            {/* Success Badge */}
            <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: "spring", stiffness: 200 }}
                className="flex items-center gap-2 mb-8 px-4 py-3 bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-xl w-fit"
            >
                <CheckCircle className="text-green-600" size={20} />
                <span className="font-semibold text-green-700 text-sm">Article Generated Successfully</span>
            </motion.div>

            {/* Article Content */}
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.2, duration: 0.6 }}
                className="article-content prose lg:prose-xl mb-10"
            >
                <ReactMarkdown>{article}</ReactMarkdown>
            </motion.div>

            {/* Critique Section */}
            {critique && (
                <div className="critique-section mt-12 pt-8 border-t-2 border-gradient">
                    <motion.button
                        onClick={() => setShowCritique(!showCritique)}
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        className="flex items-center gap-3 px-6 py-4 bg-gradient-to-r from-indigo-50 to-purple-50 hover:from-indigo-100 hover:to-purple-100 border-2 border-indigo-200 rounded-2xl transition-all w-full md:w-auto group"
                    >
                        <div className="p-2 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg">
                            <Lightbulb className="text-white" size={18} />
                        </div>
                        <span className="font-bold text-gray-800 text-lg">AI Critique & Analysis</span>
                        <motion.div
                            animate={{ rotate: showCritique ? 180 : 0 }}
                            transition={{ duration: 0.3 }}
                            className="ml-auto"
                        >
                            <ChevronDown size={20} className="text-indigo-600" />
                        </motion.div>
                    </motion.button>

                    <AnimatePresence>
                        {showCritique && (
                            <motion.div
                                initial={{ opacity: 0, height: 0 }}
                                animate={{ opacity: 1, height: "auto" }}
                                exit={{ opacity: 0, height: 0 }}
                                transition={{ duration: 0.3 }}
                                className="overflow-hidden"
                            >
                                <div className="mt-6 p-8 bg-gradient-to-br from-indigo-50/50 to-purple-50/50 backdrop-blur-sm rounded-2xl border-2 border-indigo-100 shadow-lg">
                                    <div className="flex items-center gap-3 mb-6">
                                        <div className="p-3 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl">
                                            <TrendingUp className="text-white" size={24} />
                                        </div>
                                        <div>
                                            <h4 className="font-bold text-xl text-gray-800">Expert AI Review</h4>
                                            <p className="text-sm text-gray-600">Comprehensive analysis and feedback</p>
                                        </div>
                                    </div>
                                    {renderCritiqueContent()}
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>
            )}
        </div>
    );
};

export default ArticleDisplay;
