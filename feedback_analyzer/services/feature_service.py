from typing import Tuple
from sqlalchemy.exc import SQLAlchemyError
from feedback_analyzer.models.feature import Feature
from feedback_analyzer.extensions import db
from feedback_analyzer.dtos.feedback_dto import FeedbackRequestDTO
from sqlalchemy.sql import func

class FeatureService:
    @staticmethod
    def extract_features(feedback_dto: FeedbackRequestDTO) -> Feature:
        created_features = []
        try:
            features = FeatureService.__extract_features(feedback_dto.feedback)
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
    
    @staticmethod
    def list_features():
        return db.session.query(Feature).all()
    
    @staticmethod
    def get_features_by_feedback_id(feedback_id: str):
        return db.session.query(Feature).filter_by(feedback_id=feedback_id).all()