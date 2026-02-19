from core.models import Interview, Question


class InterviewService:
    def __init__(self, session):
        self.session = session

    def get_interview_and_question(self, interview_id: str):
        interview = (
            self.session.query(Interview)
            .filter(Interview.id == interview_id)
            .with_for_update()
            .first()
        )
        if not interview:
            raise ValueError("Interview not found")

        question = (
            self.session.query(Question)
            .filter(
                Question.interview_id == interview_id,
                Question.order_index == interview.current_question_index
            )
            .first()
        )

        if not question:
            raise ValueError("No active question")

        return interview, question

    def move_to_next_question(self, interview: Interview):
        interview.current_question_index += 1

    def is_completed(self, interview: Interview) -> bool:
        total = self.session.query(Question).filter(
            Question.interview_id == interview.id
        ).count()
        return interview.current_question_index > total
