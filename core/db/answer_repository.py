from core.models import Answer, Evaluation


class AnswerRepository:
    def __init__(self, session):
        self.session = session

    def create_answer(self, answer: Answer) -> Answer:
        self.session.add(answer)
        self.session.flush()  # assigns answer.id without commit
        return answer

    def create_evaluation(self, evaluation: Evaluation):
        self.session.add(evaluation)

    def commit(self):
        self.session.commit()
