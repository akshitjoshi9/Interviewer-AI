from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship, JSON, Column

from core.models import TimestampMixin, Answer


class Evaluation(TimestampMixin, SQLModel, table=True):
    __tablename__ = "evaluations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    answer_id: UUID = Field(foreign_key="answers.id", index=True)
    score: Optional[float] = Field(default=None, ge=0, le=10)
    feedback: Optional[str] = None
    model_used: Optional[str] = Field(default=None,max_length=100)
    # Relationships
    answer: Answer = Relationship(back_populates="evaluations")
