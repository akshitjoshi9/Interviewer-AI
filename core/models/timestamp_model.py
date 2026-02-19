from datetime import datetime, timezone
from sqlmodel import SQLModel, Field


class TimestampMixin(SQLModel, table=False):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )
