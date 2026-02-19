# Interviewer-AI



# ---------------------------------------------------------
##  Which database to use:
- Use PostgreSQL as your primary database.
- Add Redis for session/state caching (recommended).
- Optional later: Vector DB (only if you need semantic retrieval).

# Your bottleneck will NOT be the DB.
It will be:
- LLM API latency
- STT processing time
- TTS generation

# I would use:

FastAPI (async)
PostgreSQL
Redis
SQLAlchemy or Tortoise ORM
Alembic migrations
Dockerized setup
Gunicorn + Uvicorn workers

# using user_metadata field instead of separate fields as below:
- in user_metadata we can store like:
{
  "average_score": 7.4,
  "strengths": ["Django", "APIs"],
  "weaknesses": ["System Design"]
}

- separate fields:
average_score: float
strengths: List[str]
weaknesses: List[str]

## Purpose of metadata field or dict for other models as below:
# Question model:

{
  "difficulty": "easy",
  "category": "technical",
  "generated_by": "llama-3.3-70b",
  "prompt_version": "v1.0",
  "skill_targeted": "Django",
  "is_followup": false,
  "expected_keywords": ["ORM", "MVC", "MTV"]
}

# Answer models:

{
  "stt_confidence": 0.89,
  "speech_duration": 24,
  "filler_words_count": 5,
  "confidence_score_voice": 7.5,
  "emotion_detected": "neutral",
  "audio_noise_level": "low"
}

# JobDescription model:

{
  "source": "linkedin_upload",
  "parsed_by": "llama-3.3-70b",
  "jd_complexity_score": 6.2,
  "embedding_model": "text-embedding-3-large",  
  "token_count": 843
}

# Interview model:

{
  "interview_type": "technical_screening",
  "mode": "voice",
  "graph_version": "v1.2",
  "total_duration_seconds": 480,
  "ai_overall_confidence": 0.81,
  "device_type": "desktop",
  "network_quality": "good"
}
