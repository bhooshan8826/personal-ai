// API Response Types
export interface Task {
  id: string
  user_id: string
  title: string
  description?: string
  priority: string
  status: string
  deadline?: string
  created_at: string
  updated_at: string
  tags: string[]
  metadata: Record<string, any>
}

export interface Note {
  id: string
  user_id: string
  title?: string
  content: string
  tags: string[]
  is_archived: boolean
  created_at: string
  updated_at: string
  metadata: Record<string, any>
}

export interface Reminder {
  id: string
  user_id: string
  task_id: string
  next_trigger: string
  recurrence?: string
  is_active: boolean
  last_triggered?: string
  created_at: string
  updated_at: string
}

export interface ChatMessage {
  id: string
  response: string
  intent?: string
  entities?: Record<string, any>
  actions?: Array<Record<string, any>>
}

export interface ChatRequest {
  message: string
  conversation_id?: string
}

export interface Intent {
  intent: string
  entities: Record<string, any>
  confidence: number
}

// Request Types
export interface CreateTaskRequest {
  title: string
  description?: string
  priority?: string
  deadline?: string
  tags?: string[]
}

export interface UpdateTaskRequest {
  title?: string
  description?: string
  priority?: string
  status?: string
  deadline?: string
  tags?: string[]
}

export interface CreateNoteRequest {
  title?: string
  content: string
  tags?: string[]
}

export interface CreateReminderRequest {
  task_id: string
  next_trigger: string
  recurrence?: string
}

// UI Types
export interface ToastMessage {
  id: string
  message: string
  type: 'success' | 'error' | 'info' | 'warning'
  duration?: number
}

export interface LoadingState {
  isLoading: boolean
  error?: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  limit: number
  offset: number
}
