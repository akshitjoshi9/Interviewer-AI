from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship, JSON, Column
from sqlalchemy import Index

from core.models import TimestampMixin, User
from conversation.constants import InterviewStatusConstant


class JobDescription(TimestampMixin, SQLModel, table=True):
    __tablename__ = "job_descriptions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(min_length=2, max_length=100, index=True)
    raw_text: str = Field(min_length=20)
    parsed_data: Dict[str, Any] = Field(
        default_factory=dict,
        sa_type=JSON
    )
    # Relationships
    interviews: List["Interview"] = Relationship(back_populates="job_description")


class Interview(TimestampMixin, SQLModel, table=True):
    __tablename__ = "interviews"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    jd_id: UUID = Field(
        foreign_key="job_descriptions.id",
        nullable=False,
        index=True
        )
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    ended_at: Optional[datetime] = None
    current_question_index: int = Field(default=1)
    total_score: Optional[float] = Field(default=0)
    max_score: Optional[float] = Field(default=0)
    percentage_score: Optional[float] = Field(default=0)
    interview_metadata: Dict[str, Any] = Field(default_factory=dict, sa_type=JSON)
    status: Optional[InterviewStatusConstant] = Field(
    default="initiated",
    index=True
    )
    # Relationships
    user: User = Relationship(back_populates="interviews")
    job_description: JobDescription = Relationship(back_populates="interviews")
    questions: List["Question"] = Relationship(back_populates="interview")

    __table_args__ = (
        Index("idx_interview_user_jd", "user_id", "jd_id"),
    )
