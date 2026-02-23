from flask import Flask
from dotenv import load_dotenv
from flask import jsonify
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
    from app.blueprints.users.routes import users_bp
    from app.blueprints.workouts.routes import workouts_bp
    
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(workouts_bp, url_prefix="/api/users/<string:user_uuid>/workouts")

    print("-------------------------------")
    print("AVAILABLE ENDPOINTS:")
    for rule in app.url_map.iter_rules():
        print(rule)
    print("-------------------------------")
    @app.get("/health")
    def health_check():
        try:
            from app.extensions import get_db
            db = get_db()
            db.command("ping")
            return jsonify({"status": "connected to mongo"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return app