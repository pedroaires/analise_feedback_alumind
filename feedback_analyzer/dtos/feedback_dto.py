from pydantic import BaseModel
from typing import List, Dict

class FeedbackRequestDTO(BaseModel):
    id: str
    feedback: str

class FeedbackResponseDTO(BaseModel):
    id: str
    feedback: str
    sentiment: str
    requested_features: List[Dict]


    @classmethod
    def from_orm(cls, feedback_obj, features_objs):
        return cls(
            id=str(feedback_obj.id),
            feedback=feedback_obj.text,
            sentiment=feedback_obj.sentiment,
            requested_features=[{"code": feat.code, "reason": feat.reason} for feat in features_objs]
        )