from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship, JSON, Column

from core.models import TimestampMixin, Question


class Answer(TimestampMixin, SQLModel, table=True):
    __tablename__ = "answers"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    question_id: UUID = Field(
        foreign_key="questions.id",
        nullable=False,
        index=True
    )
    user_id: UUID = Field(
        foreign_key="users.id",
        index=True
    )
    answer_text: Optional[str] = None
    audio_url: Optional[str] = None
    # This score helps to decide: should we trust, should we ask user to repeat, etc.
    transcription_confidence: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0
    )
    answer_metadata: Dict[str, Any] = Field(
        default_factory=dict,
        sa_type=JSON
    )
    # Relationships
    question: Question = Relationship(back_populates="answers")
    evaluations: List["Evaluation"] = Relationship(back_populates="answer")
