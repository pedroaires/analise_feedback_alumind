from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from feedback_analyzer.models.feature import Feature
from feedback_analyzer.extensions import db
from feedback_analyzer.dtos.feedback_dto import FeedbackRequestDTO
from sqlalchemy.sql import func
import uuid

class FeatureService:
    @classmethod
    def extract_features(cls, feedback_dto: FeedbackRequestDTO) -> List[Feature]:
        try:
            features = cls.__extract_features(feedback_dto.feedback)
            created_features = []
            for feat in features:
                new_feat = Feature(
                    feedback_id=feedback_dto.id,
                    code=feat["code"],
                    reason=feat["reason"],
                    created_at=func.now()
                )
                db.session.add(new_feat)
                created_features.append(new_feat)
            db.session.commit()
            return created_features
        except SQLAlchemyError as e:
            db.session.rollback()
            raise
    
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