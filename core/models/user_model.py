from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship, JSON, Column
from core.models import TimestampMixin


class User(TimestampMixin, SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    first_name: str = Field(min_length=2, max_length=20, index=True)
    last_name: str = Field(min_length=2, max_length=20, index=True)
    email: Optional[str] = Field(
        default=None,
        index=True,
        unique=True,
        max_length=30
    )
    phone: Optional[str] = Field(default=None, max_length=15)
    resume_url: Optional[str] = Field(default=None)
    user_metadata: Dict[str, Any] = Field(
        default_factory=dict,
        sa_type=JSON
    )
    # Relationships
    interviews: List["Interview"] = Relationship(back_populates="user")
