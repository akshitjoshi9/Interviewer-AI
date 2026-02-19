from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship, JSON, Column
from sqlalchemy import Index

from core.models import TimestampMixin
from .interview_model import Interview


class Question(TimestampMixin, SQLModel, table=True):
    __tablename__ = "questions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    interview_id: UUID = Field(
        foreign_key="interviews.id",
        index=True,
    )
    question_text: str = Field(min_length=2, nullable=False)
    # without order_index: db row order is not guaranteed, questions may appear in random order, etc.
    order_index: int = Field(ge=0, index=True)
    difficulty: Optional[str] = Field(
        default=None,
        max_length=20
    )
    question_metadata: Dict[str, Any] = Field(
        default_factory=dict,
        sa_type=JSON
    )
    # Relationships
    interview: Interview = Relationship(back_populates="questions")
    answers: List["Answer"] = Relationship(back_populates="question")

    __table_args__ = (
        Index(
            "idx_question_interview_order",
            "interview_id",
            "order_index",
            unique=True
        ),
    )
