from flask import Flask
from config import get_config
from feedback_analyzer.extensions import db

def create_app():
    app = Flask(__name__)
    
    config_class = get_config()
    app.config.from_object(config_class)

    db.init_app(app)

    # Registro de blueprints
    from feedback_analyzer.routes.home import home_bp
    app.register_blueprint(home_bp)
    from feedback_analyzer.routes.feedback_route import feedback_bp
    app.register_blueprint(feedback_bp)


    return app

