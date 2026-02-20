from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()


def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config.from_object('app.config.Config')

    
    # Initialize extensions
    from app.extensions import init_db
    init_db(app)
    
    # Register blueprints
    # from app.blueprints.users.routes import users_bp
    # from app.blueprints.workouts.routes import workouts_bp
    
    # app.register_blueprint(users_bp, url_prefix='/api/users')
    # app.register_blueprint(workouts_bp, url_prefix='/api/workouts')
    
    @app.route('/health')
    def health():
        return {'status': 'ok'}, 200
    
    return app
