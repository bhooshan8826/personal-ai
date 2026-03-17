import React, { useState } from 'react'
import Head from 'next/head'
import Link from 'next/link'
import { useTasks } from '@/hooks/useApi'

export default function Tasks() {
  const { tasks, loading, error, createTask, completeTask, deleteTask } = useTasks()
  const [newTaskTitle, setNewTaskTitle] = useState('')
  const [filter, setFilter] = useState('pending')
  const [showForm, setShowForm] = useState(false)

  const filteredTasks = tasks.filter((t) => filter === 'all' || t.status === filter)

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newTaskTitle.trim()) return

    try {
      await createTask(newTaskTitle)
      setNewTaskTitle('')
      setShowForm(false)
    } catch (err) {
      console.error('Failed to create task:', err)
    }
  }

  const handleCompleteTask = async (id: string) => {
    try {
      await completeTask(id)
    } catch (err) {
      console.error('Failed to complete task:', err)
    }
  }

  const handleDeleteTask = async (id: string) => {
    if (confirm('Delete this task?')) {
      try {
        await deleteTask(id)
      } catch (err) {
        console.error('Failed to delete task:', err)
      }
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'text-red-400'
      case 'medium':
        return 'text-yellow-400'
      case 'low':
        return 'text-green-400'
      default:
        return 'text-slate-400'
    }
  }

  return (
    <>
      <Head>
        <title>Tasks - Personal AI Assistant</title>
      </Head>

      <div className="min-h-screen bg-slate-900">
        {/* Navigation */}
        <nav className="bg-slate-800 border-b border-slate-700">
          <div className="max-w-7xl mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <Link href="/">
                <div className="flex items-center space-x-2 cursor-pointer">
                  <div className="text-2xl font-bold text-blue-400">⚡</div>
                  <h1 className="text-xl font-bold text-white">Tasks</h1>
                </div>
              </Link>
              <div className="flex space-x-4">
                <Link href="/chat">
                  <button className="btn-secondary">Chat</button>
                </Link>
                <Link href="/notes">
                  <button className="btn-secondary">Notes</button>
                </Link>
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="max-w-4xl mx-auto px-6 py-12">
          {/* Header */}
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-3xl font-bold text-white">My Tasks</h2>
            <button
              onClick={() => setShowForm(!showForm)}
              className="btn-primary"
            >
              + New Task
            </button>
          </div>

          {/* Create Task Form */}
          {showForm && (
            <form onSubmit={handleCreateTask} className="card mb-8">
              <div className="space-y-4">
                <input
                  type="text"
                  value={newTaskTitle}
                  onChange={(e) => setNewTaskTitle(e.target.value)}
                  placeholder="What do you need to do?"
                  className="input-field"
                  autoFocus
                />
                <div className="flex gap-3">
                  <button
                    type="submit"
                    className="btn-primary"
                    disabled={!newTaskTitle.trim()}
                  >
                    Create
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

          {/* Filters */}
          <div className="flex gap-3 mb-8">
            {['pending', 'completed', 'all'].map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`px-4 py-2 rounded-lg font-semibold transition-colors capitalize ${
                  filter === f
                    ? 'bg-blue-600 text-white'
                    : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                }`}
              >
                {f}
              </button>
            ))}
          </div>

          {/* Error */}
          {error && (
            <div className="bg-red-900 border border-red-700 text-red-100 px-4 py-3 rounded-lg mb-6">
              {error}
            </div>
          )}

          {/* Tasks List */}
          {loading ? (
            <div className="text-center py-12">
              <div className="inline-block animate-spin">⟳</div>
              <p className="text-slate-400 mt-3">Loading tasks...</p>
            </div>
          ) : filteredTasks.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-4xl mb-3">✓</div>
              <p className="text-slate-400">No tasks yet. Create one to get started!</p>
            </div>
          ) : (
            <div className="space-y-3">
              {filteredTasks.map((task) => (
                <div
                  key={task.id}
                  className="card flex items-start justify-between hover:bg-slate-750 transition-colors"
                >
                  <div className="flex-1 flex items-start gap-4">
                    <button
                      onClick={() => handleCompleteTask(task.id)}
                      className={`mt-1 w-6 h-6 rounded border-2 flex items-center justify-center flex-shrink-0 ${
                        task.status === 'completed'
                          ? 'bg-green-600 border-green-600'
                          : 'border-slate-500 hover:border-blue-500'
                      }`}
                    >
                      {task.status === 'completed' && '✓'}
                    </button>
                    <div>
                      <h3
                        className={`font-semibold text-lg ${
                          task.status === 'completed'
                            ? 'line-through text-slate-500'
                            : 'text-white'
                        }`}
                      >
                        {task.title}
                      </h3>
                      {task.description && (
                        <p className="text-slate-400 mt-1">{task.description}</p>
                      )}
                      <div className="flex gap-2 mt-2">
                        <span className={`text-xs px-2 py-1 rounded ${getPriorityColor(task.priority)}`}>
                          {task.priority}
                        </span>
                        {task.deadline && (
                          <span className="text-xs px-2 py-1 rounded bg-slate-700 text-slate-300">
                            {new Date(task.deadline).toLocaleDateString()}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                  <button
                    onClick={() => handleDeleteTask(task.id)}
                    className="btn-danger px-3 py-1 text-sm flex-shrink-0"
                  >
                    Delete
                  </button>
                </div>
              ))}
            </div>
          )}
        </main>
      </div>
    </>
  )
}
