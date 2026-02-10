# AI Interviewer System (Work in Progress)

## Overview

This project implements an **AI-powered Interviewer** using **Agentic AI concepts**, **LangGraph**, and **FastAPI**, with integrated **Speech-to-Text (STT)** and **Text-to-Speech (TTS)** capabilities powered by OpenAI models.

At a high level, the system:
1. Accepts a Job Description (JD)
2. Uses an agentic workflow to analyze the JD
3. Generates structured interview questions
4. Conducts a voice-based interview by:
   - Speaking questions aloud
   - Accepting spoken answers
   - Transcribing responses to text

⚠️ **Work in Progress**
This implementation represents an early-stage, functional prototype. Several architectural decisions are intentionally simple and may evolve as the project matures.

---

## High-Level Architecture

```
Client (UI / Frontend)
   |
   | 1. POST JD
   v
FastAPI Router
   |
   | 2. Invoke LangGraph
   v
LangGraph Agents Pipeline
   ├── parse_jd (Agent)
   └── plan_questions (Agent)
   |
   | 3. Generated Questions
   v
In-Memory Interview Engine
   |
   ├── TTS → Speak Question
   └── STT → Transcribe Answer
```

---

## Core Technologies

- **FastAPI** – API layer and request handling
- **LangGraph** – Agent orchestration and state transitions
- **LangChain / ChatOpenAI** – LLM interaction
- **OpenAI Audio APIs**
  - STT: `gpt-4o-mini-transcribe`
  - TTS: `gpt-4o-mini-tts`
- **Python TypedDict** – Structured agent state

--------------------------------------------------------------------

## Agentic Design with LangGraph

This project uses **LangGraph** to model the interview preparation process as a **stateful agent graph**.

### Why LangGraph?

- Explicit control over execution flow
- Shared, typed state across agents
- Easy extensibility for future agents (evaluation, scoring, follow-ups)

---

## State Definition

```python
class InterviewState(TypedDict):
    jd: str
    parsed_jd: dict
    questions: List[str]
```

### State Fields

| Field        | Description                                      |
|--------------|--------------------------------------------------|
| `jd`         | Raw job description text                         |
| `parsed_jd`  | Structured JD data extracted by the parser agent |
| `questions`  | Final list of generated interview questions      |
-------------------------------------------------------------------


## Agents / Nodes

### parse_jd Agent

**Purpose:**
Transforms unstructured JD text into structured data.

**Responsibilities:**
- Extracts role, skills, experience level, and priority competencies
- Enforces JSON output via LLM response formatting

**State Update:**
- Produces `parsed_jd`

--------------------------------------------------------------------

### plan_questions Agent

**Purpose:**
Generates interview questions based on structured JD data.

**Responsibilities:**
- Generates exactly 2 questions
- Orders questions from easy → hard
- Ensures voice-friendly phrasing

**State Update:**
- Produces `questions`

--------------------------------------------------------------------

## Graph Execution Flow

```
ENTRY → parse_jd → plan_questions → END
```
The graph executes linearly with a single shared state object.
Project Structure
The project is organized to clearly separate API routing, agent logic, and voice processing responsibilities.

--------------------------------------------------------------------

## Project Structure

The project is organized to clearly separate API routing, agent logic,
and voice processing responsibilities.

```text
Interviewer-AI/
├── ai/
│   ├── agents.py            # LangGraph agents (parse_jd, plan_questions)
│   ├── tts.py               # Text-to-Speech and Speech-to-Text helpers
│   ├── voice_pipeline.py    # Chatbot voice flow (Q → TTS → STT → next)
│   └── __init__.py
│
├── conversation/
│   └── routers.py           # FastAPI interview-related API endpoints
│
├── core/                    # Core utilities / shared logic (future use)
│
├── static/                  # Frontend static assets (audio, css, js)
├── templates/               # HTML templates for UI
│
├── main.py                  # FastAPI application entry point
├── requirements.txt
└── README.md
```
--------------------------------------------------------------------

## FastAPI Integration

FastAPI acts as:
- An orchestrator for interview sessions
- A bridge between HTTP requests and the LangGraph workflow
- A voice interface via STT/TTS endpoints

--------------------------------------------------------------------

## API Endpoints

### POST /interview/init

Initializes an interview session by running the LangGraph pipeline.

**Request Body**
```json
{
  "jd": "Job description text"
}
```

**Response**
```json
{
  "status": "ready"
}
```

--------------------------------------------------------------------

### GET /interview/question/audio

Returns the current interview question as an audio stream.

- Uses TTS
- Returns `completed` when questions are exhausted

--------------------------------------------------------------------

### POST /interview/answer

Accepts a spoken answer as an audio file.

**Flow**
1. Reads uploaded audio
2. Converts speech to text
3. Logs transcription
4. Advances question index

--------------------------------------------------------------------

## Voice / AI Components

### Text-to-Speech (TTS)

- Model: `gpt-4o-mini-tts`
- Converts question text to spoken audio

### Speech-to-Text (STT)

- Model: `gpt-4o-mini-transcribe`
- Transcribes candidate audio responses

--------------------------------------------------------------------

## Interview Session Management

### Current Design

- In-memory global variables
- Single interview flow at a time
- No persistence or session isolation

⚠️ Suitable only for local testing and demos.

--------------------------------------------------------------------

## Current Limitations

- No session management
- Global mutable state (not thread-safe)
- No answer evaluation or scoring
- Fixed number of questions
- No persistence layer

--------------------------------------------------------------------

## Development Status

**Status:** Active Development (Prototype)

Implemented:
- JD parsing agent
- Question planning agent
- Voice-based interview loop

Planned:
- Answer evaluation agents
- Adaptive questioning
- Persistent storage
- Real-time streaming

--------------------------------------------------------------------

## Suggestions / Improvements

- Introduce session-based state management
- Add evaluation and scoring agents
- Replace global state with Redis or database
- Improve STT streaming reliability
- Add error handling and retries


## Notes

This README documents the **current implementation only**.
Future enhancements should extend this documentation accordingly.
