from pydantic import BaseModel, Field
from typing import List

class FeatureRequestModel(BaseModel):
    code: str = Field(description="Código identificador da funcionalidade solicitada")
    reason: str = Field(description="Motivo pelo qual o usuário deseja essa funcionalidade")

class FeedbackAnalysisModel(BaseModel):
    sentiment: str = Field(description="Sentimento identificado no feedback: POSITIVO, NEUTRO ou NEGATIVO")
    requested_features: List[FeatureRequestModel] = Field(description="Lista de funcionalidades solicitadas pelo usuário")
