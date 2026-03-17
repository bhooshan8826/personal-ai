import { useState, useEffect } from 'react'
import { Task, Note, Reminder, ChatMessage } from '@/types'
import { apiClient } from '@/services/api'

export function useTasks() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const loadTasks = async (status?: string) => {
    setLoading(true)
    setError(null)
    try {
      const result = await apiClient.listTasks(status)
      setTasks(result.tasks)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load tasks')
    } finally {
      setLoading(false)
    }
  }

  const createTask = async (title: string, description?: string) => {
    try {
      const newTask = await apiClient.createTask({
        title,
        description,
        priority: 'medium',
        tags: [],
      })
      setTasks([...tasks, newTask])
      return newTask
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create task')
      throw err
    }
  }

  const completeTask = async (id: string) => {
    try {
      const updated = await apiClient.completeTask(id)
      setTasks(tasks.map((t) => (t.id === id ? updated : t)))
      return updated
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to complete task')
      throw err
    }
  }

  const deleteTask = async (id: string) => {
    try {
      await apiClient.deleteTask(id)
      setTasks(tasks.filter((t) => t.id !== id))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete task')
      throw err
    }
  }

  useEffect(() => {
    loadTasks()
  }, [])

  return { tasks, loading, error, createTask, completeTask, deleteTask, loadTasks }
}

export function useNotes() {
  const [notes, setNotes] = useState<Note[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const loadNotes = async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await apiClient.listNotes()
      setNotes(result.notes)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load notes')
    } finally {
      setLoading(false)
    }
  }

  const createNote = async (title: string, content: string, tags: string[] = []) => {
    try {
      const newNote = await apiClient.createNote({ title, content, tags })
      setNotes([...notes, newNote])
      return newNote
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create note')
      throw err
    }
  }

  const deleteNote = async (id: string) => {
    try {
      await apiClient.deleteNote(id)
      setNotes(notes.filter((n) => n.id !== id))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete note')
      throw err
    }
  }

  useEffect(() => {
    loadNotes()
  }, [])

  return { notes, loading, error, createNote, deleteNote, loadNotes }
}

export function useReminders() {
  const [reminders, setReminders] = useState<Reminder[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const loadReminders = async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await apiClient.listReminders()
      setReminders(result.reminders)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load reminders')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadReminders()
  }, [])

  return { reminders, loading, error, loadReminders }
}

export function useChat() {
  const [messages, setMessages] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const sendMessage = async (message: string) => {
    setLoading(true)
    setError(null)
    try {
      const response = await apiClient.chat(message)
      setMessages([
        ...messages,
        { role: 'user', content: message },
        { role: 'assistant', content: response.response },
      ])
      return response
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message')
      throw err
    } finally {
      setLoading(false)
    }
  }

  return { messages, loading, error, sendMessage }
}
