from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class FeatureDTO(BaseModel):
    id: UUID
    code: str
    reason: str
    
    @classmethod
    def from_orm(cls, feature_entity):
        return cls(
            id=feature_entity.id,
            code=feature_entity.code,
            reason=feature_entity.reason,
        )