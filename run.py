import uuid
from feedback_analyzer import create_app
from feedback_analyzer.extensions import db
import json
import logging
from feedback_analyzer.models.feature import Feature
from feedback_analyzer.models.feedback import Feedback
from feedback_analyzer.services.feedback_service import FeedbackService
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

app = create_app()

def populate_db(json_filepath: str):
    with app.app_context():
        with open(json_filepath, 'r', encoding='utf-8') as file:
            feedbacks_data = json.load(file)

        for feedback_item in feedbacks_data:
            feedback = Feedback(
                id=uuid.UUID(feedback_item["id"]),
                text=feedback_item["text"],
                sentiment=feedback_item["sentiment"],
            )

            for feature_item in feedback_item["requested_features"]:
                feature = Feature(
                    id=uuid.uuid4(),
                    feedback=feedback,
                    code=feature_item["code"],
                    reason=feature_item["reason"],
                )
                db.session.add(feature)

            db.session.add(feedback)

        db.session.commit()
        logging.info(f"Dados carregados com sucesso do arquivo '{json_filepath}'.")


def send_weekly_email_job():
    with app.app_context():
        logging.info("Executando job semanal de envio de email.")
        FeedbackService.send_weekly_feedback_email()

if __name__ == '__main__':
    with app.app_context():
        # para desenvolvimento apenas
        db.drop_all()
        db.create_all()
        populate_db('data/feedbacks.json')

        scheduler = BackgroundScheduler()
        # Toda sexta-feira as 17h 
        scheduler.add_job(send_weekly_email_job, 'cron', day_of_week='fri', hour=17, minute=0)
        # para testes
        scheduler.add_job(send_weekly_email_job, 'date', run_date=datetime.now()+timedelta(seconds=5))

        scheduler.start()
        logging.info("Scheduler iniciado com sucesso")
    app.run(debug=True, use_reloader=False)