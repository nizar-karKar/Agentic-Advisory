import { useState } from 'react'
import { generateArticle } from './services/api'
import ArticleDisplay from './components/ArticleDisplay'
import { Loader2, Send, BookOpen } from 'lucide-react'
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
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 text-gray-900 font-sans">
      <header className="fixed top-0 w-full bg-white/80 backdrop-blur-md border-b border-gray-100 z-50">
        <div className="max-w-4xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2 font-bold text-xl bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">
            <BookOpen className="text-indigo-600" />
            AI Medium Publisher
          </div>
        </div>
      </header>

      <main className="pt-24 pb-12 px-4 max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-extrabold mb-4 tracking-tight">
            Turn your questions into <span className="text-indigo-600">compelling stories</span>
          </h1>
          <p className="text-gray-500 text-lg">
            Powered by advanced AI agents to research, draft, and critique for you.
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-xl shadow-indigo-100/50 p-6 md:p-8 mb-8 border border-gray-100">
          <form onSubmit={handleSubmit} className="relative">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="What topic do you want to write about? (e.g., The Future of Quantum Computing)"
              className="w-full pl-6 pr-32 py-4 text-lg rounded-xl border border-gray-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all placeholder:text-gray-400"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !question.trim()}
              className="absolute right-2 top-2 bottom-2 bg-indigo-600 hover:bg-indigo-700 text-white px-6 rounded-lg font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {loading ? <Loader2 className="animate-spin" /> : <Send size={18} />}
              {loading ? 'Drafting...' : 'Generate'}
            </button>
          </form>
          {error && (
            <div className="mt-4 p-4 bg-red-50 text-red-600 rounded-lg text-sm flex items-center gap-2">
              <span className="font-bold">Error:</span> {error}
            </div>
          )}
        </div>

        {article && (
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-700">
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 md:p-12 prose-container">
              <ArticleDisplay article={article} critique={critique} />
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
