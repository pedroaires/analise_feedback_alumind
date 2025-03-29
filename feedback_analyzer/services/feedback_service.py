from typing import List, Tuple
from sqlalchemy.exc import SQLAlchemyError
from feedback_analyzer.models.feedback import Feedback
from feedback_analyzer.extensions import db
from feedback_analyzer.dtos.feedback_dto import FeedbackRequestDTO
from feedback_analyzer.services.feature_service import FeatureService
from sqlalchemy.sql import func

class FeedbackService:

    @classmethod
    def process_feedback(cls, feedback_data):
        try: 
            text = feedback_data.feedback
            sentiment = cls.extract_sentiment(text)
            features = FeatureService.extract_features(text)
            
            feedback = Feedback(
                text=text,
                sentiment=sentiment,
                requested_features=features
            )

            db.session.add(feedback)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
        return feedback
            
    @staticmethod
    def extract_sentiment(text: str) -> Tuple[str, str]:
        # TODO: implement
        return "Positivo", "Por que o mundo é bom"
    
    @staticmethod
    def list_feedbacks() -> List[Feedback]:
        query = db.session.query(Feedback)
        return query.order_by(Feedback.created_at.desc()).all()
    
    @staticmethod
    def list_feedbacks_with_features():
        return Feedback.query.options(db.joinedload(Feedback.requested_features)).all()