import io
from core.config import settings, openai_client


def text_to_speech_bytes(text: str) -> bytes:
    response = openai_client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )
    return response.read()


async def speech_to_text(audio_bytes: bytes) -> str:
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "audio.webm"

    transcript = openai_client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",
        file=audio_file,
        language="en"
    )

    return transcript.text

def speech_to_text_sync(audio_bytes: bytes) -> str:
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "audio.webm"

    transcript = openai_client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",
        file=audio_file,
        language="en"
    )

    return transcript.text
