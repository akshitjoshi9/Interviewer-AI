from fastapi import APIRouter, UploadFile, File, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse
from fastapi.concurrency import run_in_threadpool
import io
from sqlmodel import Session

from ai.agents import build_graph, build_evaluation_graph
from ai.tts import text_to_speech_bytes, speech_to_text, speech_to_text_sync
from core.db.session import get_session_ml_engine
from core.models import Interview, JobDescription, Question, Answer, Evaluation, User
from conversation.constants import InterviewStatusConstant
from core.services import finalize_interview, InterviewService
from core.db.answer_repository import AnswerRepository
from ai.compiled_graphs import INTERVIEW_GRAPH, EVALUATION_GRAPH
from core.services import run_evaluation


router = APIRouter()

interview_graph = build_graph()

QUESTIONS = {}


@router.post("/interview/init")
async def init_interview(
    payload: dict,
    session: Session = Depends(get_session_ml_engine),
):
    """
    1. Save JD
    2. Run LangGraph
    3. Create Interview
    4. Save Questions in DB
    """

    jd_text = payload.get("jd")
    user_id = payload.get("user_id")
    user_id = "cf0b09e0-fd1a-4c8c-9361-1179b43c9120"
    if not jd_text:
        return {"status": "error", "message": "JD is required"}

    if not user_id:
        return {"status": "error", "message": "user_id is required"}

    # Run LangGraph
    result = INTERVIEW_GRAPH.invoke({
        "jd": jd_text,
        "parsed_jd": {},
        "questions": []
    })

    parsed_data = result.get("parsed_jd", {})
    questions_list = result.get("questions", [])

    # Save Job Description
    job = JobDescription(
        title=parsed_data.get("role", "Generated JD"),
        raw_text=jd_text,
        parsed_data=parsed_data
    )

    session.add(job)
    session.commit()
    session.refresh(job)

    # Create Interview
    interview = Interview(
        user_id=user_id,
        jd_id=job.id,
        status=InterviewStatusConstant.READY,
        interview_metadata={
            "parsed_jd": parsed_data
        }
    )

    session.add(interview)
    session.commit()
    session.refresh(interview)

    # Save Questions
    question_objects = []

    for index, question_text in enumerate(questions_list, start=1):
        question = Question(
            interview_id=interview.id,
            question_text=question_text,
            order_index=index,
            difficulty="easy" if index == 1 else "hard"
        )

        question_objects.append(question)

    session.add_all(question_objects)
    session.commit()

    print("\n=========== QUESTIONS SAVED IN DB ===========\n")
    for q in question_objects:
        print(f"Q{q.order_index}: {q.question_text}")

    return {
        "status": "ready",
        "interview_id": interview.id
    }


@router.get("/interview/question/audio/{interview_id}")
async def speak_question(
    interview_id: str,
    session: Session = Depends(get_session_ml_engine),
):
    # Get interview
    interview = session.query(Interview).filter(
        Interview.id == interview_id
    ).first()

    if not interview:
        return {"status": "error", "message": "Interview not found"}

    # Get next question
    question = (
        session.query(Question)
        .filter(
            Question.interview_id == interview_id,
            Question.order_index == interview.current_question_index
        )
        .first()
    )

    if not question:
        return {"status": "completed"}

    # Correct threadpool usage
    audio_bytes = await run_in_threadpool(
        text_to_speech_bytes,
        question.question_text
    )

    return StreamingResponse(
        io.BytesIO(audio_bytes),
        media_type="audio/mpeg"
    )

@router.post("/interview/answer/{interview_id}")
async def receive_answer(
    interview_id: str,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    session: Session = Depends(get_session_ml_engine),
):
    interview_service = InterviewService(session)
    repo = AnswerRepository(session)

    with session.begin():
        interview, question = interview_service.get_interview_and_question(interview_id)

        audio_bytes = await file.read()
        text = await run_in_threadpool(
            speech_to_text_sync,
            audio_bytes
        )

        answer = repo.create_answer(
            Answer(
                question_id=question.id,
                user_id=interview.user_id,
                answer_text=text,
                transcription_confidence=1.0,
            )
        )
        interview_service.move_to_next_question(interview)

    # Schedule evaluation AFTER commit
    background_tasks.add_task(
        run_evaluation,
        answer.id,
        question.question_text,
        text,
        interview.interview_metadata["parsed_jd"]
    )

    if interview_service.is_completed(interview):
        finalize_interview(interview, session)
        return {"status": "completed"}

    return {"status": "ok"}


@router.get("/interview/{interview_id}/results")
def interview_results(
    interview_id: str,
    session: Session = Depends(get_session_ml_engine),
):

    interview = session.query(Interview).filter(
        Interview.id == interview_id
    ).first()

    if not interview or interview.status != "completed":
        return {"status": "error", "message": "Interview not completed"}

    data = []
    total_score = 0
    max_score = 0

    # Fetch all questions for this interview
    questions = (
        session.query(Question)
        .filter(Question.interview_id == interview_id)
        .order_by(Question.order_index)
        .all()
    )

    for q in questions:
        answer = (
            session.query(Answer)
            .filter(Answer.question_id == q.id)
            .first()
        )

        evaluation = (
            session.query(Evaluation)
            .filter(Evaluation.answer_id == answer.id)
            .first()
            if answer else None
        )

        # Add score to total_score and max_score
        if evaluation:
            total_score += evaluation.score
            max_score += 10  # assuming each question is scored out of 10

        data.append({
            "question": q.question_text,
            "answer": answer.answer_text if answer else None,
            "score": evaluation.score if evaluation else None,
            "feedback": evaluation.feedback if evaluation else None,
        })

    # Calculate percentage score
    if max_score > 0:
        percentage_score = (total_score / max_score) * 100
    else:
        percentage_score = 0

    # Update the interview with the calculated scores (optional)
    interview.total_score = total_score
    interview.max_score = max_score
    interview.percentage_score = percentage_score
    session.commit()

    return {
        "status": "ok",
        "summary": {
            "total_score": total_score,
            "max_score": max_score,
            "percentage": percentage_score,
            "decision": interview.interview_metadata.get("decision"),
        },
        "results": data
    }
