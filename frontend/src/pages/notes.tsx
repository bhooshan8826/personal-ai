import React, { useState } from 'react'
import Head from 'next/head'
import Link from 'next/link'
import { useNotes } from '@/hooks/useApi'

export default function Notes() {
  const { notes, loading, error, createNote, deleteNote } = useNotes()
  const [newNoteContent, setNewNoteContent] = useState('')
  const [newNoteTitle, setNewNoteTitle] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')

  const filteredNotes = notes.filter(
    (n) =>
      !n.is_archived &&
      (n.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        n.content.toLowerCase().includes(searchQuery.toLowerCase()))
  )

  const handleCreateNote = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newNoteContent.trim()) return

    try {
      await createNote(newNoteTitle, newNoteContent)
      setNewNoteTitle('')
      setNewNoteContent('')
      setShowForm(false)
    } catch (err) {
      console.error('Failed to create note:', err)
    }
  }

  const handleDeleteNote = async (id: string) => {
    if (confirm('Delete this note?')) {
      try {
        await deleteNote(id)
      } catch (err) {
        console.error('Failed to delete note:', err)
      }
    }
  }

  return (
    <>
      <Head>
        <title>Notes - Personal AI Assistant</title>
      </Head>

      <div className="min-h-screen bg-slate-900">
        {/* Navigation */}
        <nav className="bg-slate-800 border-b border-slate-700">
          <div className="max-w-7xl mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <Link href="/">
                <div className="flex items-center space-x-2 cursor-pointer">
                  <div className="text-2xl font-bold text-blue-400">⚡</div>
                  <h1 className="text-xl font-bold text-white">Notes</h1>
                </div>
              </Link>
              <div className="flex space-x-4">
                <Link href="/chat">
                  <button className="btn-secondary">Chat</button>
                </Link>
                <Link href="/tasks">
                  <button className="btn-secondary">Tasks</button>
                </Link>
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="max-w-6xl mx-auto px-6 py-12">
          {/* Header */}
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-3xl font-bold text-white">My Notes</h2>
            <button
              onClick={() => setShowForm(!showForm)}
              className="btn-primary"
            >
              + New Note
            </button>
          </div>

          {/* Search */}
          <div className="mb-8">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search notes..."
              className="input-field max-w-md"
            />
          </div>

          {/* Create Note Form */}
          {showForm && (
            <form onSubmit={handleCreateNote} className="card mb-8">
              <div className="space-y-4">
                <input
                  type="text"
                  value={newNoteTitle}
                  onChange={(e) => setNewNoteTitle(e.target.value)}
                  placeholder="Note title (optional)"
                  className="input-field"
                  autoFocus
                />
                <textarea
                  value={newNoteContent}
                  onChange={(e) => setNewNoteContent(e.target.value)}
                  placeholder="Write your note here..."
                  className="input-field min-h-32 resize-none"
                />
                <div className="flex gap-3">
                  <button
                    type="submit"
                    className="btn-primary"
                    disabled={!newNoteContent.trim()}
                  >
                    Save Note
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowForm(false)}
                    className="btn-secondary"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </form>
          )}

          {/* Error */}
          {error && (
            <div className="bg-red-900 border border-red-700 text-red-100 px-4 py-3 rounded-lg mb-6">
              {error}
            </div>
          )}

          {/* Notes Grid */}
          {loading ? (
            <div className="text-center py-12">
              <div className="inline-block animate-spin">⟳</div>
              <p className="text-slate-400 mt-3">Loading notes...</p>
            </div>
          ) : filteredNotes.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-4xl mb-3">📝</div>
              <p className="text-slate-400">
                {searchQuery ? 'No notes match your search.' : 'No notes yet. Create one to get started!'}
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredNotes.map((note) => (
                <div key={note.id} className="card flex flex-col">
                  {note.title && (
                    <h3 className="text-lg font-semibold text-white mb-2">{note.title}</h3>
                  )}
                  <p className="text-slate-300 text-sm line-clamp-3 mb-4 flex-1">
                    {note.content}
                  </p>
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-slate-500">
                      {new Date(note.created_at).toLocaleDateString()}
                    </span>
                    <button
                      onClick={() => handleDeleteNote(note.id)}
                      className="btn-danger px-3 py-1 text-sm"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </main>
      </div>
    </>
  )
}
