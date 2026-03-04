import os
from datetime import datetime, timedelta
from flask import Flask, app, request, jsonify, session, redirect, url_for, render_template, flash
from dotenv import load_dotenv
from app.services.users.service import UserService
from app.services.workouts.service import WorkoutService
from app.services.presets.service import PresetService
from app.services.meals.service import MealService
from app.services.meals.models import MealEntry, MealItem
from app.services.water.service import WaterService
from app.services.water.models import WaterItem
from app.extensions import init_db, get_db

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    from app.extensions import init_db
    init_db(app)


    '''------- AUTH API ROUTES -------'''

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
    
    '''------- WORKOUT API ROUTES -------'''

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
            return redirect(url_for("dashboard_page"))

        return redirect(url_for("dashboard_page"))
    
    @app.post("/api/workouts/update")
    def handle_update_workout():
        user_uuid = session.get("user_uuid")
        if not user_uuid:
            return redirect(url_for("login_page"))

        workout_uuid = request.form.get("workout_uuid")
        if not workout_uuid:
            flash("Missing workout ID.", "error")
            return redirect(url_for("workouts_page"))

        workout_data = {
            "date": request.form.get("date"),
            "type": request.form.get("type"),
            "duration": request.form.get("duration"),
            "reps": request.form.get("reps"),
            "weight": request.form.get("weight"),
            "calories": request.form.get("calories")
        }

        try:
            updated = WorkoutService.update_workout(user_uuid, workout_uuid, workout_data)
            
            if updated:
                flash("Workout updated successfully!", "success")
            else:
                flash("Workout not found or unauthorized.", "error")
                
        except Exception as e:
            flash(f"Error updating workout: {str(e)}", "error")

        return redirect(url_for("workouts_page"))
    
    @app.post("/api/workouts/delete")
    def handle_delete_workout():
        user_uuid = session.get("user_uuid")
        if not user_uuid:
            return redirect(url_for("login_page"))

        workout_uuid = request.form.get("workout_uuid")
        
        if not workout_uuid:
            flash("Workout ID is required.", "error")
            return redirect(url_for("workouts_page"))

        try:
            success = WorkoutService.delete_workout(user_uuid, workout_uuid)
            if success:
                flash("Workout deleted successfully!", "success")
            else:
                flash("Workout not found.", "error")
        except Exception as e:
            flash(f"An error occurred while deleting the workout: {str(e)}", "error")

        return redirect(url_for("workouts_page"))
        

    '''------- MEAL API ROUTES -------'''

    @app.post("/api/meals/add")
    def handle_add_meal():
        user_uuid = session.get("user_uuid")
        if not user_uuid:
            return redirect(url_for("login_page"))

        try:
            date_str = request.form.get("date")
            name = request.form.get("name")
            calories = request.form.get("calories")
            protein = request.form.get("protein")
            carbs = request.form.get("carbs")
            fat = request.form.get("fat")

            date = datetime.fromisoformat(date_str)

            meal_item = MealItem(
                type=name,
                calories=float(calories),
                protein=float(protein),
                carbs=float(carbs),
                fat=float(fat)
            )
            meal_entry = MealEntry(items=[meal_item])

            MealService.update_meals(user_uuid, date, meal_entry)
            flash("Meal saved successfully!", "success")
        except Exception as e:
            flash(f"Error saving meal: {str(e)}", "error")

        return redirect(url_for("nutrition_page"))

    '''------- WATER API ROUTES -------'''

    @app.post("/api/water/add")
    def handle_add_water():
        user_uuid = session.get("user_uuid")
        if not user_uuid:
            return redirect(url_for("login_page"))

        try:
            date_str = request.form.get("date")
            amount = request.form.get("amount")

            date = datetime.fromisoformat(date_str)
            water_item = WaterItem(time=datetime.now(), amount=int(amount))

            WaterService.update_water(user_uuid, date, water_item)
            flash("Water intake saved successfully!", "success")
        except Exception as e:
            flash(f"Error saving water intake: {str(e)}", "error")

        return redirect(url_for("nutrition_page"))

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

        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        meal_data = MealService.get_user_meals(user_uuid, today)
        total_calories = 0
        for entry in meal_data.meals:
            for item in entry.items:
                total_calories += item.calories

        water_data = WaterService.get_user_water(user_uuid, today)
        total_water = sum(w.amount for w in water_data.water)

        tdee = UserService.get_tdee_for_user(user_uuid)

        return render_template("dashboard.html", workouts=workouts, weekly_count=weekly_count, recommendation=recommendation, total_calories=int(total_calories), total_water=total_water, tdee=tdee)
    
    @app.route("/workouts")
    def workouts_page():
        user_uuid = session.get("user_uuid")
        if not user_uuid:
            return redirect(url_for("login_page"))
        
        search_date = request.args.get('date')
        all_workouts = WorkoutService.get_workouts_by_user(user_uuid)

        if search_date:
            workouts = [w for w in all_workouts if w.get('date', '').startswith(search_date)]
        else:
            workouts = all_workouts

        return render_template("workout_list.html", workouts=workouts)
    
    @app.route("/workouts/edit/<workout_id>")
    def edit_workout_page(workout_id):
        user_uuid = session.get("user_uuid")
        if not user_uuid:
            return redirect(url_for("login_page"))
        
        workout = WorkoutService.get_workout_by_uuid(user_uuid, workout_id)
        if not workout:
            flash("Workout not found.", "error")
            return redirect(url_for("workouts_page"))
        
        raw_date = workout.get("date")
        
        if raw_date and isinstance(raw_date, str):
            workout["date_str"] = raw_date[:10]
        else:
            from datetime import datetime
            workout["date_str"] = datetime.now().strftime('%Y-%m-%d')
        
        return render_template("edit_workout.html", workout=workout)
    
    @app.route("/nutrition")
    def nutrition_page():
        user_uuid = session.get("user_uuid")
        if not user_uuid:
            return redirect(url_for("login_page"))

        search_date = request.args.get('date')
        if search_date:
            date = datetime.fromisoformat(search_date)
        else:
            date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        selected_date = date.strftime('%Y-%m-%d')
        today = datetime.now().strftime('%Y-%m-%d')

        meal_data = MealService.get_user_meals(user_uuid, date)
        meals = []
        total_calories = 0
        for entry in meal_data.meals:
            for item in entry.items:
                meals.append({"meal": item.model_dump()})
                total_calories += item.calories

        water_data = WaterService.get_user_water(user_uuid, date)
        water_entries = water_data.water
        total_water = sum(w.amount for w in water_entries)

        return render_template("nutrition.html",
            meals=meals,
            water_entries=water_entries,
            total_calories=int(total_calories),
            total_water=total_water,
            selected_date=selected_date,
            today=today
        )

    @app.route("/meals")
    def meals_page():
        user_uuid = session.get("user_uuid")
        if not user_uuid:
            return redirect(url_for("login_page"))

        search_date = request.args.get('date')
        if search_date:
            date = datetime.fromisoformat(search_date)
        else:
            date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        meal_data = MealService.get_user_meals(user_uuid, date)
        meals = []
        for entry in meal_data.meals:
            for item in entry.items:
                meals.append({"meal": item.model_dump()})

        return render_template("meals.html", meals=meals)

    @app.route("/meals/add")
    def add_meal_page():
        user_uuid = session.get("user_uuid")
        if not user_uuid:
            return redirect(url_for("login_page"))

        prefill = {
            "date": datetime.now().strftime('%Y-%m-%d'),
            "name": request.args.get("name", ""),
            "calories": request.args.get("calories", ""),
            "protein": request.args.get("protein", ""),
            "carbs": request.args.get("carbs", ""),
            "fat": request.args.get("fat", ""),
        }
        return render_template("add_meal.html", prefill=prefill)

    @app.route("/water/add")
    def add_water_page():
        user_uuid = session.get("user_uuid")
        if not user_uuid:
            return redirect(url_for("login_page"))
        return render_template("add_water.html")

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