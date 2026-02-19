from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
import json
from core.config import llm


# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
llm = llm


class InterviewState(TypedDict):
    jd: str
    parsed_jd: dict
    questions: List[str]


class EvaluationState(TypedDict):
    question: str
    answer: str
    parsed_jd: dict
    evaluation: dict


def parse_jd(state: InterviewState):
    prompt = f"""
Extract structured data from this Job Description.

Return JSON with:
skills (list),
experience_level,
role,
priority_competencies (list)

JD:
{state['jd']}
"""
    res = llm.invoke(prompt, response_format={"type": "json_object"})
    parsed = json.loads(res.content)

    print("\n=== PARSED JD ===")
    print(json.dumps(parsed, indent=2))

    return {"parsed_jd": parsed}


def plan_questions(state: InterviewState):
    jd = state["parsed_jd"]

    prompt = f"""
You are an AI interviewer.

Based on the following Job Description details, generate interview questions.

Return output strictly in JSON format.

JSON schema:
{{
  "questions": ["question1", "question2"]
}}

JD Details:
Role: {jd.get('role')}
Skills: {jd.get('skills')}
Experience: {jd.get('experience_level')}
Competencies: {jd.get('priority_competencies')}

Rules:
- 2 questions only
- Easy → Hard
- Voice friendly
"""

    res = llm.invoke(prompt, response_format={"type": "json_object"})
    data = json.loads(res.content)

    questions = data["questions"]

    print("\n=== GENERATED QUESTIONS ===")
    for i, q in enumerate(questions, 1):
        print(f"Q{i}: {q}")

    return {"questions": questions}


def evaluate_answer(state: EvaluationState):
    question = state["question"]
    answer = state["answer"]
    jd = state["parsed_jd"]

    prompt = f"""
    You are a strict AI technical interviewer.

    Evaluate the candidate's answer.

    SCORING RULES:
    - Score must be between 0 to 10
    - Consider correctness, clarity, depth, relevance to JD
    - Be realistic (do NOT always give high scores)

    Return strictly JSON.

    JSON Schema:
    {{
    "score": number (0-10),
    "feedback": "detailed explanation on candidate answer wrt question and experience",
    "strengths": "what was good",
    "improvements": "what was missing or weak"
    }}

    Job Context:
    Role: {jd.get("role")}
    Skills: {jd.get("skills")}
    Experience: {jd.get("experience_level")}
    Competencies: {jd.get("priority_competencies")}

    Question:
    {question}

    Candidate Answer:
    {answer}
    """
    # breakpoint()
    res = llm.invoke(
        prompt,
        response_format={"type": "json_object"}
    )

    data = json.loads(res.content)

    print("\n=== EVALUATION RESULT ===")
    print(json.dumps(data, indent=2))

    return {"evaluation": data}


def build_graph():
    graph = StateGraph(InterviewState)
    graph.add_node("parse_jd", parse_jd)
    graph.add_node("plan_questions", plan_questions)

    graph.set_entry_point("parse_jd")
    graph.add_edge("parse_jd", "plan_questions")
    graph.add_edge("plan_questions", END)

    return graph.compile()

def build_evaluation_graph():
    graph = StateGraph(EvaluationState)

    graph.add_node("evaluate_answer", evaluate_answer)

    graph.set_entry_point("evaluate_answer")
    graph.add_edge("evaluate_answer", END)

    return graph.compile()
