from enum import Enum


class InterviewStatusConstant(str, Enum):
    """ 
    Constants for the interview status.
    1. CREATED: seassion created, jd saved, agent not started yet.
    2. READY: questions generated, interview prepared, waiting for candidate.
    3. IN_PROGRESS: candidate answering questions, STT running, Questions index advancing.
    4. COMPLETED: all questions answered, no more input expected.
    5. FAILED: LLM failure, STT failure, unexpected crash.
    """

    CREATED = "created"
    READY = "ready"
    IN_PROGRESS = "in progress"
    COMPLETED = "completed"
    FAILED = "failed"
 