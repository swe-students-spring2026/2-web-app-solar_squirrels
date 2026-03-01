from flask import Blueprint, render_template

workouts_bp = Blueprint(
    "workouts",
    __name__,
    url_prefix="/workouts",
    template_folder="templates",
    static_folder="static",
)


@workouts_bp.get("/list")
def workout_list_page():
    return render_template("workouts.html")


@workouts_bp.get("/add")
def add_workout_page():
    return render_template("add_workout.html")