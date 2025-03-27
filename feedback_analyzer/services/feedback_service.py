from typing import List, Tuple
from sqlalchemy.exc import SQLAlchemyError
from feedback_analyzer.models.feedback import Feedback
from feedback_analyzer.extensions import db
from feedback_analyzer.dtos.feedback_dto import FeedbackRequestDTO
from feedback_analyzer.services.feature_service import FeatureService
from sqlalchemy.sql import func

class FeedbackService:
    @classmethod
    def perform_classification(cls, feedback: FeedbackRequestDTO) -> Feedback:
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

    @classmethod
    def process_feedback(cls, feedback_data):
        feedback = cls.perform_classification(feedback_data)
        features = FeatureService.extract_features(feedback_data)
        return feedback, features
            
    @staticmethod
    def __classify_feedback(text: str) -> Tuple[str, str]:
        return "Positivo", "Por que o mundo é bom"
    
    @classmethod
    def list_feedbacks(cls) -> List[Feedback]:
        query = db.session.query(Feedback)
        return query.order_by(Feedback.created_at.desc()).all()