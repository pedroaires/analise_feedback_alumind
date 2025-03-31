import uuid
from feedback_analyzer import create_app
from feedback_analyzer.extensions import db
import json

from feedback_analyzer.models.feature import Feature
from feedback_analyzer.models.feedback import Feedback


def load_json_to_db(json_filepath: str):
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
        print(f"Dados carregados com sucesso do arquivo '{json_filepath}'.")


app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        load_json_to_db('data/feedbacks.json')
    app.run(debug=True)