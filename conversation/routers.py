from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
import io

from ai.agents import build_graph
from ai.tts import text_to_speech_bytes, speech_to_text

router = APIRouter()

interview_graph = build_graph()

QUESTIONS = {}
current_question_index = 1


@router.post("/interview/init")
async def init_interview(payload: dict):
    """
        1. Receives JD from page-1
        2. Runs LangGraph agents
        3. Generates interview questions
        4. Stores them in memory
    """
    global QUESTIONS, current_question_index

    jd_text = payload.get("jd")

    if not jd_text:
        return {"status": "error", "message": "JD is required"}

    result = interview_graph.invoke({
        "jd": payload["jd"],
        "parsed_jd": {},
        "questions": []
    })

    QUESTIONS = {
        i + 1: q for i, q in enumerate(result["questions"])
    }
    current_question_index = 1

    print("\n================ INTERVIEW INITIALIZED ================\n")
    print("FINAL QUESTION LIST USED BY INTERVIEW ENGINE:\n")
    for i, q in QUESTIONS.items():
        print(f"Q{i}: {q}")
    print("\n=======================================================\n")

    return {"status": "ready"}


@router.get("/interview/question/audio")
def speak_question():
    global current_question_index

    if current_question_index not in QUESTIONS:
        return {"status": "completed"}

    question_text = QUESTIONS[current_question_index]
    audio_bytes = text_to_speech_bytes(question_text)

    return StreamingResponse(
        io.BytesIO(audio_bytes),
        media_type="audio/mpeg"
    )


@router.post("/interview/answer")
async def receive_answer(file: UploadFile = File(...)):
    global current_question_index

    audio_bytes = await file.read()
    text = await speech_to_text(audio_bytes)

    print(f"\n===== ANSWER FOR QUESTION {current_question_index} =====")
    print(text)
    print("=========================================\n")

    current_question_index += 1

    return {"status": "ok"}
