from typing import List
from sqlalchemy.exc import SQLAlchemyError
from feedback_analyzer.models.feedback import Feedback
from feedback_analyzer.extensions import db
from feedback_analyzer.dtos.feedback_dto import FeedbackRequestDTO
from sqlalchemy.sql import func

class FeedbackService:
    @staticmethod
    def perform_classification(feedback: FeedbackRequestDTO) -> Feedback:
        classification = FeedbackService.__classify_feedback(feedback.feedback)
        new_feedback = Feedback()
        try:
            new_feedback = Feedback(
                id=feedback.id,
                text=feedback.feedback,
                sentiment=classification,
                created_at=func.now()

            )
            db.session.add(new_feedback)
            db.session.commit()
            return new_feedback
        except SQLAlchemyError as e:
            db.session.rollback()
            raise
            

    def __classify_feedback(text: str) -> str:
        return "Positivo", "Por que o mundo é bom"
    
    @staticmethod
    def list_feedbacks() -> List[Feedback]:
        return db.session.query(Feedback).all()