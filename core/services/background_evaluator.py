from ai.compiled_graphs import EVALUATION_GRAPH
from core.models import Evaluation
from core.db.session import SessionLocalML


def run_evaluation(
    answer_id: str,
    question_text: str,
    answer_text: str,
    parsed_jd: dict,
):
    session = SessionLocalML()

    try:
        result = EVALUATION_GRAPH.invoke({
            "question": question_text,
            "answer": answer_text,
            "parsed_jd": parsed_jd
        })

        evaluation = Evaluation(
            answer_id=answer_id,
            score=result["evaluation"]["score"],
            feedback=result["evaluation"]["feedback"],
            strengths=result["evaluation"].get("strengths"),
            improvements=result["evaluation"].get("improvements"),
            model_used="gpt-4o",
        )

        session.add(evaluation)
        session.commit()

    except Exception as e:
        session.rollback()
        print("Evaluation failed:", e)

    finally:
        session.close()
