from pydantic import BaseModel

class FeedbackRequestDTO(BaseModel):
    id: str
    feedback: str

class FeedbackResponseDTO(BaseModel):
    id: str
    feedback: str
    sentiment: str
    reason: str

    @classmethod
    def from_orm(cls, feedback_obj):
        return cls(
            id=feedback_obj.id,
            feedback=feedback_obj.text,
            sentiment=feedback_obj.sentiment,
            reason=feedback_obj.reason
        )