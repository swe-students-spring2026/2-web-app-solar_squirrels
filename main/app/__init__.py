import os
import uuid as uuid_lib
from datetime import datetime, timezone
from flask import Flask, request, jsonify, session, redirect, url_for, render_template, flash
from dotenv import load_dotenv
from app.blueprints.users.service import UserService
from app.blueprints.workouts.service import WorkoutService
from app.extensions import init_db, get_db

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    from app.extensions import init_db
    init_db(app)

    from app.blueprints.users.routes import users_bp
    from app.blueprints.workouts.routes import workouts_bp
    
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(workouts_bp, url_prefix="/api/users/<string:user_uuid>/workouts")

    print("-------------------------------")
    print("AVAILABLE ENDPOINTS:")
    for rule in app.url_map.iter_rules():
        print(rule)
    print("-------------------------------")


    '''------- AUTH ROUTES -------'''

    @app.post("/api/auth/register")
    def register():
        data = request.json
        if not data.get("username") or not data.get("password"):
            return jsonify({"error": "Username and password required"}), 400
            
        try:
            user = UserService.create_user(data)
            return jsonify({"message": "User registered", "uuid": user.uuid}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.post("/api/auth/login")
    def login():
        data = request.form if request.form else request.json
        user = UserService.authenticate_user(
            data.get("username"), 
            data.get("password")
        )
        
        if user:
            session["user_uuid"] = user["uuid"]
            return redirect(url_for('dashboard'))
        
        return jsonify({"error": "Invalid username or password"}), 401

    @app.post("/api/auth/logout")
    def logout():
        session.clear()
        return jsonify({"message": "Logged out"}), 200
    
    '''------- WORKOUT ROUTES -------'''

    @app.post("/api/workouts/add")
    def handle_add_workout():
        user_uuid = session.get("user_uuid")
        if not user_uuid:
            return redirect(url_for("login_page"))

        workout_data = {
            "type": request.form.get("type"),
            "duration": request.form.get("duration"),
            "reps": request.form.get("reps"),
            "weight": request.form.get("weight"),
            "calories": request.form.get("calories")
        }

        try:
            WorkoutService.create_workout(user_uuid, workout_data)
            flash("Workout saved successfully!", "success")
        except Exception as e:
            flash(f"Error saving workout: {str(e)}", "error")
            return redirect(url_for("dashboard"))

        return redirect(url_for("dashboard"))
    
    





    '''------- PAGE ROUTES -------'''

    @app.route("/")
    def login_page():
        return app.send_static_file("index.html")

    @app.route("/dashboard")
    def dashboard():
        user_uuid = session.get("user_uuid")
        if not user_uuid:
            return redirect(url_for("login_page"))
        
        return render_template("dashboard.html")
    
    app.route("/workout/add-workout")
    def add_workout():
        user_uuid = session.get("user_uuid")
        if not user_uuid:
            return redirect(url_for("login_page"))

        return render_template("add_workout.html")

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