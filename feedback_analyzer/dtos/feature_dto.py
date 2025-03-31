from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class FeatureDTO(BaseModel):
    code: str
    reason: str
    
    @classmethod
    def from_orm(cls, feature_entity):
        return cls(
            code=feature_entity.code,
            reason=feature_entity.reason,
        )