from feedback_analyzer.extensions import db
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(UUID, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(50))
    created_at = db.Column(db.Datetime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<Feedback {self.id}>'
    