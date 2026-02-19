import os
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from conversation.routers import router as interview_router
from ai.voice_pipeline import VoiceChatSession

from core.config import openai_client


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(interview_router, prefix="/api")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/interview")
def interview(request: Request):
    return templates.TemplateResponse("interview.html", {"request": request})

@app.get("/chat")
def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.websocket("/ws/chat")
async def chat_ws(ws: WebSocket):
    await ws.accept()
    print("Voice Chatbot Connected")

    session = VoiceChatSession()
    greeting = session.start()
    await ws.send_json({"text": greeting})

    try:
        while True:
            data = await ws.receive_json()
            user_text = data.get("text")

            if not user_text:
                continue

            print(user_text)
            ai_text = session.reply(user_text)
            print(ai_text)

            await ws.send_json({
                "text": ai_text
            })

    except WebSocketDisconnect:
        print("Voice Chatbot Disconnected")

@app.get("/interview/result/{interview_id}")
def interview_result_page(request: Request, interview_id: str):
    return templates.TemplateResponse(
        "interview_result.html",
        {
            "request": request,
            "interview_id": interview_id,
            "title": "Interview Results"
        }
    )
