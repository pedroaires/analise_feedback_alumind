from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from feedback_analyzer.models.feature import Feature
from feedback_analyzer.extensions import db
from feedback_analyzer.dtos.feedback_dto import FeedbackRequestDTO
from sqlalchemy.sql import func
import uuid

class FeatureService:
    @classmethod
    def extract_features(cls, text) -> List[Feature]:
        features = []
        for feature in cls.__extract_features(text):
            features.append(Feature(
                code=feature["code"],
                reason=feature["reason"]
            )) 
        return features
            
    
    @staticmethod
    def __extract_features(text: str):
        # TODO: implement
        features = [{"code": "editar_algo", "reason": "pq sim"}]
        return features
    
    @classmethod
    def list_features(cls, feedback_id: Optional[str] = None):
        query = db.session.query(Feature)
        if feedback_id:
            try:
                feedback_uuid = uuid.UUID(feedback_id)
                query = query.filter(Feature.feedback_id == feedback_uuid)
            except ValueError:
                # invalid UUID format
                return []
        return query.order_by(Feature.created_at.desc()).all()
    
    @staticmethod
    def get_features_by_feedback_id(feedback_id: str):
        return db.session.query(Feature).filter_by(feedback_id=feedback_id).all()