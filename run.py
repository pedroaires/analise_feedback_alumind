from feedback_analyzer import create_app
from feedback_analyzer.extensions import db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all() 
    app.run(debug=True)