"""
SQLAlchemy ORM models for the application
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, ForeignKey, JSON, Index
from sqlalchemy.orm import relationship
from database.database import Base


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    preferences = Column(JSON, default={})

    # Relationships
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")
    reminders = relationship("Reminder", back_populates="user", cascade="all, delete-orphan")
    email_drafts = relationship("EmailDraft", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")


class Task(Base):
    """Task model"""
    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), index=True)
    title = Column(String(255), index=True)
    description = Column(Text, nullable=True)
    priority = Column(String(10), default="medium")  # low, medium, high
    status = Column(String(20), default="pending")  # pending, completed, cancelled
    deadline = Column(DateTime, nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tags = Column(JSON, default=[])
    metadata = Column(JSON, default={})

    # Relationships
    user = relationship("User", back_populates="tasks")
    reminder = relationship("Reminder", back_populates="task", uselist=False, cascade="all, delete-orphan")

    # Indexes for common queries
    __table_args__ = (
        Index("ix_task_user_status", "user_id", "status"),
        Index("ix_task_user_deadline", "user_id", "deadline"),
    )


class Note(Base):
    """Note model"""
    __tablename__ = "notes"

    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), index=True)
    title = Column(String(255), nullable=True, index=True)
    content = Column(Text)
    tags = Column(JSON, default=[])
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = Column(JSON, default={})

    # Relationships
    user = relationship("User", back_populates="notes")

    # Indexes
    __table_args__ = (
        Index("ix_note_user_tags", "user_id"),
    )


class Reminder(Base):
    """Reminder model"""
    __tablename__ = "reminders"

    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), index=True)
    task_id = Column(String(36), ForeignKey("tasks.id"), unique=True)
    next_trigger = Column(DateTime, index=True)
    recurrence = Column(String(20), nullable=True)  # none, daily, weekly, monthly
    is_active = Column(Boolean, default=True)
    last_triggered = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = Column(JSON, default={})

    # Relationships
    user = relationship("User", back_populates="reminders")
    task = relationship("Task", back_populates="reminder")

    # Indexes
    __table_args__ = (
        Index("ix_reminder_user_next_trigger", "user_id", "next_trigger"),
    )


class EmailDraft(Base):
    """Email draft model"""
    __tablename__ = "email_drafts"

    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), index=True)
    subject = Column(String(255))
    to = Column(String(255))
    cc = Column(String(255), nullable=True)
    bcc = Column(String(255), nullable=True)
    body = Column(Text)
    tone = Column(String(50), default="professional")
    status = Column(String(20), default="draft")  # draft, queued, sent
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = Column(JSON, default={})

    # Relationships
    user = relationship("User", back_populates="email_drafts")


class AuditLog(Base):
    """Audit log model"""
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), index=True)
    action = Column(String(100), index=True)  # create, update, delete, read
    entity_type = Column(String(50))  # Task, Note, Reminder, etc.
    entity_id = Column(String(36), index=True)
    changes = Column(JSON, default={})
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)

    # Relationships
    user = relationship("User", back_populates="audit_logs")

    # Indexes
    __table_args__ = (
        Index("ix_audit_user_timestamp", "user_id", "timestamp"),
        Index("ix_audit_entity", "entity_type", "entity_id"),
    )


class ConversationHistory(Base):
    """Conversation history model"""
    __tablename__ = "conversation_history"

    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), index=True)
    role = Column(String(20))  # user, assistant
    content = Column(Text)
    context = Column(JSON, default={})  # intent, entities, etc.
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    __table_args__ = (
        Index("ix_conversation_user_timestamp", "user_id", "timestamp"),
    )
