from feedback_analyzer.extensions import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<Feedback {self.id}>'
    