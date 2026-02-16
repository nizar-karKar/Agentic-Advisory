import { useState } from 'react'
import { generateArticle } from './services/api'
import ArticleDisplay from './components/ArticleDisplay'
import { Loader2, Send, BookOpen, Sparkles, Stars, Zap } from 'lucide-react'
import { motion } from 'framer-motion'
import './App.css'

function App() {
  const [question, setQuestion] = useState('')
  const [article, setArticle] = useState(null)
  const [critique, setCritique] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!question.trim()) return

    setLoading(true)
    setError(null)
    setArticle(null)
    setCritique(null)

    try {
      const result = await generateArticle(question)
      setArticle(result.final_answer)
      setCritique(result.critique)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-violet-50 via-indigo-50 to-purple-100 text-gray-900 font-sans relative overflow-hidden">
      {/* Animated Background Gradients */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-purple-400 to-pink-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-br from-indigo-400 to-blue-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse" style={{ animationDelay: '2s' }}></div>
        <div className="absolute top-40 left-1/2 w-80 h-80 bg-gradient-to-br from-violet-400 to-purple-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse" style={{ animationDelay: '4s' }}></div>
      </div>

      {/* Floating Particles */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        {[...Array(20)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-1 h-1 bg-indigo-400 rounded-full opacity-30"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
            animate={{
              y: [0, -30, 0],
              opacity: [0.3, 0.6, 0.3],
            }}
            transition={{
              duration: 3 + Math.random() * 2,
              repeat: Infinity,
              delay: Math.random() * 2,
            }}
          />
        ))}
      </div>

      {/* Enhanced Header with Glassmorphism */}
      <motion.header
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ type: "spring", stiffness: 100 }}
        className="fixed top-0 w-full glass-card border-b border-white/20 z-50"
      >
        <div className="max-w-5xl mx-auto px-4 h-20 flex items-center justify-between">
          <motion.div
            className="flex items-center gap-3"
            whileHover={{ scale: 1.05 }}
            transition={{ type: "spring", stiffness: 400 }}
          >
            <div className="p-2 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl shadow-lg float-animation">
              <BookOpen className="text-white" size={28} />
            </div>
            <div>
              <h1 className="font-extrabold text-2xl gradient-text">AI Medium Publisher</h1>
              <p className="text-xs text-gray-600 font-medium">Powered by Advanced AI</p>
            </div>
          </motion.div>

          <div className="hidden md:flex items-center gap-6 text-sm">
            <div className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gradient-to-r from-indigo-50 to-purple-50 border border-indigo-100">
              <Sparkles className="text-indigo-600" size={16} />
              <span className="font-semibold text-gray-700">AI-Powered</span>
            </div>
          </div>
        </div>
      </motion.header>

      <main className="pt-32 pb-12 px-4 max-w-5xl mx-auto relative z-10">
        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r from-indigo-100 to-purple-100 border border-indigo-200 mb-6">
            <Stars className="text-indigo-600" size={18} />
            <span className="text-sm font-semibold text-indigo-700">Agentic AI Writing Assistant</span>
          </div>

          <h1 className="text-5xl md:text-7xl font-black mb-6 tracking-tight leading-tight">
            Turn Ideas into
            <br />
            <span className="gradient-text">Compelling Stories</span>
          </h1>
          <p className="text-gray-600 text-lg md:text-xl max-w-2xl mx-auto leading-relaxed">
            Harness the power of advanced AI agents to research, draft, and critique
            professional articles in seconds.
          </p>
        </motion.div>

        {/* Input Form with Enhanced Design */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="glass-card rounded-3xl p-8 md:p-10 mb-12 shadow-2xl hover:shadow-indigo-200/50 transition-shadow duration-300"
        >
          <form onSubmit={handleSubmit} className="relative">
            <div className="relative">
              <div className="absolute left-6 top-1/2 -translate-y-1/2 pointer-events-none">
                <Zap className="text-indigo-400" size={24} />
              </div>
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="What topic do you want to explore? (e.g., The Future of Quantum Computing)"
                className="w-full pl-16 pr-40 py-6 text-lg rounded-2xl border-2 border-gray-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/20 outline-none transition-all placeholder:text-gray-400 bg-white/80 backdrop-blur-sm font-medium shine-effect"
                disabled={loading}
              />
              <motion.button
                type="submit"
                disabled={loading || !question.trim()}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="absolute right-3 top-1/2 -translate-y-1/2 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white px-8 py-4 rounded-xl font-bold transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 shadow-lg shadow-indigo-500/30"
              >
                {loading ? (
                  <>
                    <Loader2 className="animate-spin" size={20} />
                    <span>Crafting...</span>
                  </>
                ) : (
                  <>
                    <Send size={20} />
                    <span>Generate</span>
                  </>
                )}
              </motion.button>
            </div>
          </form>

          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-6 p-5 bg-gradient-to-r from-red-50 to-pink-50 border-l-4 border-red-500 text-red-700 rounded-xl text-sm flex items-center gap-3 shadow-sm"
            >
              <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
              <div>
                <span className="font-bold">Error:</span> {error}
              </div>
            </motion.div>
          )}

          {/* Feature Pills */}
          <div className="mt-8 flex flex-wrap gap-3 justify-center">
            <div className="px-4 py-2 rounded-full bg-white/60 backdrop-blur-sm border border-indigo-100 text-sm font-medium text-gray-700 flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              AI Research
            </div>
            <div className="px-4 py-2 rounded-full bg-white/60 backdrop-blur-sm border border-purple-100 text-sm font-medium text-gray-700 flex items-center gap-2">
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
              Smart Writing
            </div>
            <div className="px-4 py-2 rounded-full bg-white/60 backdrop-blur-sm border border-pink-100 text-sm font-medium text-gray-700 flex items-center gap-2">
              <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse"></div>
              Expert Critique
            </div>
          </div>
        </motion.div>

        {/* Article Display with Animations */}
        {article && (
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, type: "spring" }}
            className="animate-slide-in"
          >
            <div className="glass-card rounded-3xl p-10 md:p-14 prose-container shadow-2xl border-2 border-white/50">
              <ArticleDisplay article={article} critique={critique} />
            </div>
          </motion.div>
        )}
      </main>

      {/* Footer */}
      <footer className="relative z-10 py-8 text-center text-gray-600 text-sm">
        <p className="flex items-center justify-center gap-2">
          Made with <Sparkles size={16} className="text-indigo-500" /> by AI Agents
        </p>
      </footer>
    </div>
  )
}

export default App
