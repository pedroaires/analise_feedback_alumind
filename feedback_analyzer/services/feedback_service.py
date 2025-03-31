from datetime import datetime
from typing import List, Tuple
from sqlalchemy.exc import SQLAlchemyError
from feedback_analyzer.llm.llm_service import LLMService
from feedback_analyzer.models.feature import Feature
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
            llm_response = LLMService.analyze_feedback(text)

            feedback = Feedback(
                text=text,
                sentiment=llm_response["sentiment"],
                requested_features=[
                    Feature(
                        code=feat["code"], 
                        reason=feat["reason"]
                        ) for feat in llm_response["requested_features"]
                ]
            )

            db.session.add(feedback)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
        return feedback
    
    @classmethod
    def get_feedback_by_id(cls, feedback_id):
        return Feedback.query.filter_by(id=feedback_id).first()

    
    @staticmethod
    def list_feedbacks() -> List[Feedback]:
        query = db.session.query(Feedback)
        return query.order_by(Feedback.created_at.desc()).all()
    
    @staticmethod
    def list_feedbacks_with_features():
        return Feedback.query.options(db.joinedload(Feedback.requested_features)).all()
    
    @classmethod
    def generate_metrics(cls, start_date=None, end_date=None):
        query = db.session.query(Feedback)

        if start_date:
            start_date = datetime.fromisoformat(start_date)
            query = query.filter(Feedback.created_at >= start_date)

        if end_date:
            end_date = datetime.fromisoformat(end_date)
            query = query.filter(Feedback.created_at <= end_date)

        total_feedbacks = query.count()

        sentiment_counts = query.with_entities(
            Feedback.sentiment,
            func.count(Feedback.sentiment)
        ).group_by(Feedback.sentiment).all()

        feature_counts = db.session.query(
            Feature.code,
            func.count(Feature.code).label('count')
        ).join(Feedback.requested_features)\
         .filter(Feedback.id.in_([f.id for f in query]))\
         .group_by(Feature.code)\
         .order_by(func.count(Feature.code).desc())\
         .limit(10)\
         .all()

        sentiment_data = {sentiment: count for sentiment, count in sentiment_counts}

        return {
            "total_feedbacks": total_feedbacks,
            "sentiments": {
                "positive": sentiment_data.get("POSITIVO", 0),
                "neutral": sentiment_data.get("NEUTRO", 0),
                "negative": sentiment_data.get("NEGATIVO", 0)
            },
            "top_features": [
                {"code": code, "count": count} for code, count in feature_counts
            ]
        }
    
