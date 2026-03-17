import React, { useState } from 'react'
import Link from 'next/link'
import Head from 'next/head'

export default function Home() {
  const [isLoading, setIsLoading] = useState(false)

  return (
    <>
      <Head>
        <title>Personal AI Assistant</title>
        <meta name="description" content="Local-first AI assistant" />
      </Head>

      <div className="min-h-screen flex flex-col">
        {/* Navigation */}
        <nav className="bg-slate-800 border-b border-slate-700">
          <div className="max-w-7xl mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div className="text-2xl font-bold text-blue-400">⚡</div>
                <h1 className="text-xl font-bold text-white">Personal AI</h1>
              </div>
              <div className="flex space-x-4">
                <Link href="/chat">
                  <button className="btn-primary">Chat</button>
                </Link>
                <Link href="/tasks">
                  <button className="btn-secondary">Tasks</button>
                </Link>
                <Link href="/notes">
                  <button className="btn-secondary">Notes</button>
                </Link>
                <Link href="/settings">
                  <button className="btn-secondary">Settings</button>
                </Link>
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="flex-1">
          <div className="max-w-7xl mx-auto px-6 py-12">
            {/* Hero Section */}
            <div className="text-center mb-12">
              <h2 className="text-4xl font-bold text-white mb-4">
                Welcome to Your Personal AI Assistant
              </h2>
              <p className="text-xl text-slate-300 mb-8">
                Local-first, private, and intelligent. Powered by Llama 3.
              </p>
              <Link href="/chat">
                <button className="btn-primary text-lg px-8 py-4">
                  Start Chatting
                </button>
              </Link>
            </div>

            {/* Quick Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
              <div className="card">
                <div className="text-3xl font-bold text-blue-400 mb-2">📋</div>
                <h3 className="text-lg font-semibold text-white mb-1">Tasks</h3>
                <p className="text-slate-300">Track your to-dos</p>
                <Link href="/tasks">
                  <button className="btn-secondary w-full mt-4">View</button>
                </Link>
              </div>

              <div className="card">
                <div className="text-3xl font-bold text-purple-400 mb-2">📝</div>
                <h3 className="text-lg font-semibold text-white mb-1">Notes</h3>
                <p className="text-slate-300">Save your ideas</p>
                <Link href="/notes">
                  <button className="btn-secondary w-full mt-4">View</button>
                </Link>
              </div>

              <div className="card">
                <div className="text-3xl font-bold text-yellow-400 mb-2">🔔</div>
                <h3 className="text-lg font-semibold text-white mb-1">Reminders</h3>
                <p className="text-slate-300">Never forget again</p>
                <Link href="/chat">
                  <button className="btn-secondary w-full mt-4">Set</button>
                </Link>
              </div>

              <div className="card">
                <div className="text-3xl font-bold text-green-400 mb-2">💬</div>
                <h3 className="text-lg font-semibold text-white mb-1">Chat</h3>
                <p className="text-slate-300">Talk to your AI</p>
                <Link href="/chat">
                  <button className="btn-primary w-full mt-4">Chat Now</button>
                </Link>
              </div>
            </div>

            {/* Features Section */}
            <div className="bg-slate-800 border border-slate-700 rounded-lg p-8">
              <h3 className="text-2xl font-bold text-white mb-6">How It Works</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div>
                  <div className="text-4xl font-bold text-blue-400 mb-3">1</div>
                  <h4 className="text-lg font-semibold text-white mb-2">Chat</h4>
                  <p className="text-slate-300">
                    Tell your AI assistant what you need in natural language.
                  </p>
                </div>
                <div>
                  <div className="text-4xl font-bold text-blue-400 mb-3">2</div>
                  <h4 className="text-lg font-semibold text-white mb-2">Understand</h4>
                  <p className="text-slate-300">
                    The AI understands your intent and extracts relevant information.
                  </p>
                </div>
                <div>
                  <div className="text-4xl font-bold text-blue-400 mb-3">3</div>
                  <h4 className="text-lg font-semibold text-white mb-2">Execute</h4>
                  <p className="text-slate-300">
                    Tasks, reminders, and notes are created and organized automatically.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </main>

        {/* Footer */}
        <footer className="bg-slate-800 border-t border-slate-700">
          <div className="max-w-7xl mx-auto px-6 py-8">
            <div className="flex justify-between items-center">
              <p className="text-slate-400">
                © 2024 Personal AI Assistant. All data stays local.
              </p>
              <div className="flex space-x-6">
                <a href="#" className="text-slate-400 hover:text-white">
                  Docs
                </a>
                <a href="#" className="text-slate-400 hover:text-white">
                  GitHub
                </a>
                <a href="#" className="text-slate-400 hover:text-white">
                  Support
                </a>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </>
  )
}
