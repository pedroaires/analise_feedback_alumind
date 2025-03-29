from pydantic import BaseModel, Field
from typing import List, Dict
from feedback_analyzer.dtos.feature_dto import FeatureDTO
from uuid import UUID
class FeedbackRequestDTO(BaseModel):
    id: str
    feedback: str

class FeedbackResponseDTO(BaseModel):
    id: UUID
    feedback: str
    sentiment: str
    requested_features: List[FeatureDTO] = Field(default_factory=list)
    
    @classmethod
    def from_orm(cls, feedback_entity):
        return cls(
            id=feedback_entity.id,
            feedback=feedback_entity.text,
            sentiment=feedback_entity.sentiment,
            requested_features=[FeatureDTO.from_orm(feature) for feature in feedback_entity.requested_features]
        )

