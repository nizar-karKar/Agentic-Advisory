import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { ChevronDown, ChevronUp, AlertCircle, CheckCircle } from 'lucide-react';

const ArticleDisplay = ({ article, critique }) => {
    const [showCritique, setShowCritique] = useState(false);

    if (!article) return null;

    return (
        <div className="article-container">
            <div className="article-content prose lg:prose-xl">
                <ReactMarkdown>{article}</ReactMarkdown>
            </div>

            {critique && (
                <div className="critique-section mt-8 border-t border-gray-200 pt-6">
                    <button
                        onClick={() => setShowCritique(!showCritique)}
                        className="flex items-center gap-2 text-sm font-medium text-gray-500 hover:text-gray-700 transition-colors"
                    >
                        {showCritique ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                        {showCritique ? 'Hide Critique & Analysis' : 'Show Critique & Analysis'}
                    </button>

                    {showCritique && (
                        <div className="mt-4 bg-gray-50 rounded-lg p-6 text-sm text-gray-700 animate-in fade-in slide-in-from-top-2 duration-300">
                            <h4 className="font-semibold mb-3 flex items-center gap-2">
                                <AlertCircle size={16} className="text-blue-500" />
                                AI Critique
                            </h4>
                            {/* Check if critique is a dictionary/object or string and render comfortably */}
                            {typeof critique === 'object' ? (
                                <pre className="whitespace-pre-wrap font-mono text-xs bg-gray-100 p-2 rounded">
                                    {JSON.stringify(critique, null, 2)}
                                </pre>
                            ) : (
                                <p>{critique}</p>
                            )}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default ArticleDisplay;
