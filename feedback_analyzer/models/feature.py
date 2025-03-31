from feedback_analyzer.extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

class Feature(db.Model):
    __tablename__ = 'features'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    feedback_id = db.Column(UUID(as_uuid=True), ForeignKey("feedbacks.id", ondelete="CASCADE"), nullable=False)
    code = db.Column(db.Text, nullable=False)
    reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    feedback = relationship("Feedback", back_populates="requested_features")
    def __repr__(self):
        return f'<Feature {self.id}>'
    