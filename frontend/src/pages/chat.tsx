import React, { useState, useRef, useEffect } from 'react'
import Head from 'next/head'
import Link from 'next/link'
import { useChat } from '@/hooks/useApi'

export default function Chat() {
  const { messages, loading, error, sendMessage } = useChat()
  const [inputValue, setInputValue] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!inputValue.trim()) return

    const input = inputValue
    setInputValue('')

    try {
      await sendMessage(input)
    } catch (err) {
      console.error('Failed to send message:', err)
    }
  }

  return (
    <>
      <Head>
        <title>Chat - Personal AI Assistant</title>
      </Head>

      <div className="min-h-screen flex flex-col bg-slate-900">
        {/* Navigation */}
        <nav className="bg-slate-800 border-b border-slate-700">
          <div className="max-w-7xl mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <Link href="/">
                <div className="flex items-center space-x-2 cursor-pointer">
                  <div className="text-2xl font-bold text-blue-400">⚡</div>
                  <h1 className="text-xl font-bold text-white">Personal AI</h1>
                </div>
              </Link>
              <div className="flex space-x-4">
                <Link href="/tasks">
                  <button className="btn-secondary">Tasks</button>
                </Link>
                <Link href="/notes">
                  <button className="btn-secondary">Notes</button>
                </Link>
              </div>
            </div>
          </div>
        </nav>

        {/* Chat Container */}
        <main className="flex-1 max-w-4xl w-full mx-auto flex flex-col py-8">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto px-6 py-4 mb-6">
            {messages.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-center">
                <div className="text-5xl mb-6">💬</div>
                <h2 className="text-2xl font-bold text-white mb-3">Start Chatting</h2>
                <p className="text-slate-400 max-w-md mb-8">
                  Tell me about your tasks, ideas, or anything else. I'll help you
                  organize and remember.
                </p>
                <div className="bg-slate-800 rounded-lg p-6 max-w-md">
                  <p className="text-slate-300 font-semibold mb-3">Try asking:</p>
                  <ul className="text-left text-slate-400 space-y-2">
                    <li>• Create a task to review the report by Friday</li>
                    <li>• Save a note about project ideas</li>
                    <li>• Remind me to email the team tomorrow</li>
                  </ul>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                {messages.map((msg, idx) => (
                  <div
                    key={idx}
                    className={`flex ${
                      msg.role === 'user' ? 'justify-end' : 'justify-start'
                    }`}
                  >
                    <div
                      className={`max-w-xs lg:max-w-md px-4 py-3 rounded-lg ${
                        msg.role === 'user'
                          ? 'bg-blue-600 text-white'
                          : 'bg-slate-700 text-slate-100'
                      }`}
                    >
                      <p>{msg.content}</p>
                    </div>
                  </div>
                ))}
                {loading && (
                  <div className="flex justify-start">
                    <div className="bg-slate-700 text-slate-100 px-4 py-3 rounded-lg">
                      <div className="flex space-x-2">
                        <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-100"></div>
                        <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-200"></div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>

          {/* Input */}
          <div className="px-6">
            {error && (
              <div className="bg-red-900 border border-red-700 text-red-100 px-4 py-3 rounded-lg mb-4">
                {error}
              </div>
            )}
            <form onSubmit={handleSubmit} className="flex gap-3">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Tell me something..."
                className="input-field flex-1"
                disabled={loading}
              />
              <button
                type="submit"
                className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                disabled={loading || !inputValue.trim()}
              >
                Send
              </button>
            </form>
            <p className="text-xs text-slate-400 mt-3">
              Your data stays locally. No external data sharing.
            </p>
          </div>
        </main>
      </div>
    </>
  )
}
