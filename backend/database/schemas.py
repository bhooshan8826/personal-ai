"""
Pydantic request/response schemas
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr


# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    preferences: Optional[Dict[str, Any]] = None


class UserResponse(UserBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    preferences: Dict[str, Any]

    class Config:
        from_attributes = True


# Task Schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    deadline: Optional[datetime] = None
    tags: List[str] = []


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    deadline: Optional[datetime] = None
    tags: Optional[List[str]] = None


class TaskResponse(TaskBase):
    id: str
    user_id: str
    status: str
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any]

    class Config:
        from_attributes = True


# Note Schemas
class NoteBase(BaseModel):
    title: Optional[str] = None
    content: str
    tags: List[str] = []


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None
    is_archived: Optional[bool] = None


class NoteResponse(NoteBase):
    id: str
    user_id: str
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any]

    class Config:
        from_attributes = True


# Reminder Schemas
class ReminderBase(BaseModel):
    task_id: str
    next_trigger: datetime
    recurrence: Optional[str] = None


class ReminderCreate(ReminderBase):
    pass


class ReminderUpdate(BaseModel):
    next_trigger: Optional[datetime] = None
    recurrence: Optional[str] = None
    is_active: Optional[bool] = None


class ReminderResponse(ReminderBase):
    id: str
    user_id: str
    is_active: bool
    last_triggered: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Email Draft Schemas
class EmailDraftBase(BaseModel):
    subject: str
    to: str
    cc: Optional[str] = None
    bcc: Optional[str] = None
    body: str
    tone: str = "professional"


class EmailDraftCreate(EmailDraftBase):
    pass


class EmailDraftUpdate(BaseModel):
    subject: Optional[str] = None
    to: Optional[str] = None
    cc: Optional[str] = None
    bcc: Optional[str] = None
    body: Optional[str] = None
    tone: Optional[str] = None
    status: Optional[str] = None


class EmailDraftResponse(EmailDraftBase):
    id: str
    user_id: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Chat Message Schemas
class ChatMessage(BaseModel):
    role: str  # user or assistant
    content: str
    context: Optional[Dict[str, Any]] = None


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    id: str
    response: str
    intent: Optional[str] = None
    entities: Optional[Dict[str, Any]] = None
    actions: Optional[List[Dict[str, Any]]] = None


# Intent Detection Schemas
class IntentRequest(BaseModel):
    message: str


class IntentResponse(BaseModel):
    intent: str
    entities: Dict[str, Any]
    confidence: float


# Search Schemas
class SearchQuery(BaseModel):
    query: str
    type: Optional[str] = None  # notes, tasks, all
    limit: int = 10


class SearchResult(BaseModel):
    id: str
    type: str
    title: Optional[str]
    content: str
    score: float
    metadata: Dict[str, Any]


class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime


# Pagination
class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 20

    class Config:
        ge = {"page": 1, "page_size": 1}
