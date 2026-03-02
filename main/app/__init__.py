import os
from datetime import datetime, timedelta
from flask import Flask, app, request, jsonify, session, redirect, url_for, render_template, flash
from dotenv import load_dotenv
from app.services.users.service import UserService
from app.services.workouts.service import WorkoutService
from app.services.presets.service import PresetService
from app.extensions import init_db, get_db

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    from app.extensions import init_db
    init_db(app)

    print("-------------------------------")
    print("AVAILABLE ENDPOINTS:")
    for rule in app.url_map.iter_rules():
        print(rule)
    print("-------------------------------")


    '''------- AUTH ROUTES -------'''

    @app.post("/api/auth/register")
    def register():
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Username and password required", "error")
            return redirect(url_for("login_page"))
            
        try:
            user = UserService.create_user({
                "username": username,
                "password": password
            })
            
            session["user_uuid"] = user.uuid
            
            return redirect(url_for("onboarding"))
            
        except Exception as e:
            flash(f"Registration failed: {str(e)}", "error")
            return redirect(url_for("login_page"))
        
    @app.post("/api/auth/onboarding")
    def handle_onboarding():
        user_uuid = session.get("user_uuid")
        if not user_uuid:
            return redirect(url_for("login_page"))

        try:
            update_data = {
                "age": request.form.get("age"),
                "height": request.form.get("height"),
                "weight": request.form.get("weight"),
                "activity": request.form.get("activity"),
                "goals": request.form.get("goals")
            }

            updated_user = UserService.update_user(user_uuid, update_data)
            
            if not updated_user:
                flash("User not found", "error")
                return redirect(url_for("login_page"))

            flash("Profile updated!", "success")
            return redirect(url_for("dashboard_page"))

        except Exception as e:
            flash(f"Profile update failed: {str(e)}", "error")
            return redirect(url_for("onboarding"))
        
    @app.post("/api/auth/login")
    def login():
        data = request.form
        user = UserService.authenticate_user(
            data.get("username"), 
            data.get("password")
        )
        
        if user:
            session["user_uuid"] = user["uuid"]
            return redirect(url_for("dashboard_page"))
        
        flash("Invalid username or password", "error")
        return redirect(url_for("login_page"))

    @app.post("/api/auth/logout")
    def logout():
        session.clear()
        flash("You have been logged out.", "info")
        return redirect(url_for("login_page"))
    
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
        return render_template("index.html")

    @app.route("/dashboard")
    def dashboard_page():
        user_uuid = session.get("user_uuid")
        if not user_uuid:
            return redirect(url_for("login_page"))
        
        user = UserService.get_user_by_uuid(user_uuid)
        if not user or not user.activity:
            return redirect(url_for("onboarding"))
        recommendation = PresetService.get_preset_for_user(user.activity)

        workouts = WorkoutService.get_workouts_by_user(user_uuid)
        week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        weekly_count = sum(1 for item in workouts if item.get('date', '')[:10] >= week_ago)
        
        return render_template("dashboard.html", workouts=workouts, weekly_count=weekly_count, recommendation=recommendation)
    
    @app.route("/register")
    def register_page():
        return render_template("registration.html")
    
    @app.route("/onboarding")
    def onboarding():
        user_uuid = session.get("user_uuid")
        if not user_uuid:
            return redirect(url_for("login_page"))
        
        return render_template("onboarding.html")

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