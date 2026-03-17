import axios, { AxiosInstance } from 'axios'
import { Task, Note, Reminder, ChatMessage, ChatRequest, Intent } from '@/types'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

class APIClient {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('API Error:', error)
        throw error
      }
    )
  }

  // Chat
  async chat(message: string, conversationId?: string): Promise<ChatMessage> {
    const response = await this.client.post<ChatMessage>('/api/v1/chat', {
      message,
      conversation_id: conversationId,
    } as ChatRequest)
    return response.data
  }

  async analyzeIntent(message: string): Promise<Intent> {
    const response = await this.client.post<Intent>('/api/v1/intent', {
      message,
    } as ChatRequest)
    return response.data
  }

  // Tasks
  async listTasks(
    status?: string,
    priority?: string,
    limit = 50,
    offset = 0
  ): Promise<{ tasks: Task[]; total: number }> {
    const response = await this.client.get('/api/v1/tasks', {
      params: { status, priority, limit, offset },
    })
    return response.data
  }

  async createTask(task: any): Promise<Task> {
    const response = await this.client.post<Task>('/api/v1/tasks', task)
    return response.data
  }

  async getTask(id: string): Promise<Task> {
    const response = await this.client.get<Task>(`/api/v1/tasks/${id}`)
    return response.data
  }

  async updateTask(id: string, task: any): Promise<Task> {
    const response = await this.client.put<Task>(`/api/v1/tasks/${id}`, task)
    return response.data
  }

  async deleteTask(id: string): Promise<void> {
    await this.client.delete(`/api/v1/tasks/${id}`)
  }

  async completeTask(id: string): Promise<Task> {
    const response = await this.client.put<Task>(
      `/api/v1/tasks/${id}/complete`
    )
    return response.data
  }

  async searchTasks(q: string): Promise<Task[]> {
    const response = await this.client.get<Task[]>('/api/v1/tasks/_search', {
      params: { q },
    })
    return response.data
  }

  async getTaskStats(): Promise<Record<string, any>> {
    const response = await this.client.get<Record<string, any>>(
      '/api/v1/tasks/_stats'
    )
    return response.data
  }

  // Notes
  async listNotes(
    archived = false,
    limit = 50,
    offset = 0
  ): Promise<{ notes: Note[]; total: number }> {
    const response = await this.client.get('/api/v1/notes', {
      params: { archived, limit, offset },
    })
    return response.data
  }

  async createNote(note: any): Promise<Note> {
    const response = await this.client.post<Note>('/api/v1/notes', note)
    return response.data
  }

  async getNote(id: string): Promise<Note> {
    const response = await this.client.get<Note>(`/api/v1/notes/${id}`)
    return response.data
  }

  async updateNote(id: string, note: any): Promise<Note> {
    const response = await this.client.put<Note>(`/api/v1/notes/${id}`, note)
    return response.data
  }

  async deleteNote(id: string): Promise<void> {
    await this.client.delete(`/api/v1/notes/${id}`)
  }

  async searchNotes(q: string, tags?: string[]): Promise<Note[]> {
    const response = await this.client.get<Note[]>('/api/v1/notes/_search', {
      params: { q, tags },
    })
    return response.data
  }

  async archiveNote(id: string): Promise<Note> {
    const response = await this.client.put<Note>(
      `/api/v1/notes/${id}/archive`
    )
    return response.data
  }

  // Reminders
  async listReminders(
    activeOnly = true,
    limit = 50,
    offset = 0
  ): Promise<{ reminders: Reminder[]; total: number }> {
    const response = await this.client.get('/api/v1/reminders', {
      params: { active_only: activeOnly, limit, offset },
    })
    return response.data
  }

  async createReminder(reminder: any): Promise<Reminder> {
    const response = await this.client.post<Reminder>('/api/v1/reminders', reminder)
    return response.data
  }

  async getReminder(id: string): Promise<Reminder> {
    const response = await this.client.get<Reminder>(`/api/v1/reminders/${id}`)
    return response.data
  }

  async updateReminder(id: string, reminder: any): Promise<Reminder> {
    const response = await this.client.put<Reminder>(
      `/api/v1/reminders/${id}`,
      reminder
    )
    return response.data
  }

  async deleteReminder(id: string): Promise<void> {
    await this.client.delete(`/api/v1/reminders/${id}`)
  }

  async getUpcomingReminders(hours = 24): Promise<Reminder[]> {
    const response = await this.client.get<Reminder[]>(
      '/api/v1/reminders/_upcoming',
      { params: { hours } }
    )
    return response.data
  }

  async triggerReminder(id: string): Promise<Reminder> {
    const response = await this.client.post<Reminder>(
      `/api/v1/reminders/${id}/_trigger`
    )
    return response.data
  }

  async snoozeReminder(id: string, minutes = 15): Promise<Reminder> {
    const response = await this.client.post<Reminder>(
      `/api/v1/reminders/${id}/_snooze`,
      { minutes }
    )
    return response.data
  }

  // Health
  async getHealth(): Promise<Record<string, any>> {
    const response = await this.client.get('/api/v1/health')
    return response.data
  }
}

export const apiClient = new APIClient()
