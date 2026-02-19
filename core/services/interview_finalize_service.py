from datetime import datetime, timezone
from fastapi import Depends
from sqlmodel import Session

from core.db.session import get_session_ml_engine
from core.models import Interview, Question, Answer, Evaluation


def finalize_interview(interview: Interview, session: Session = Depends(get_session_ml_engine), ):

    interview.status = "completed"
    interview.ended_at = datetime.now(timezone.utc)
    session.commit()
