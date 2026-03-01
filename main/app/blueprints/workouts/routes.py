<<<<<<< HEAD
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
=======
from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from app.blueprints.workouts.service import WorkoutService

workouts_bp = Blueprint("workouts", __name__)


@workouts_bp.route("/", methods=["POST"])
def create_workout(user_uuid):
    try:
        workout = WorkoutService.create_workout(user_uuid, request.json)
        return jsonify(workout), 201

    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400


@workouts_bp.route("/", methods=["GET"])
def get_workouts(user_uuid):
    workouts = WorkoutService.get_workouts_by_user(user_uuid)
    return jsonify(workouts), 200


@workouts_bp.route("/<string:workout_uuid>", methods=["GET"])
def get_workout(user_uuid, workout_uuid):
    workout = WorkoutService.get_workout_by_uuid(user_uuid, workout_uuid)

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    return jsonify(workout), 200
>>>>>>> 2bea88b175f2b7614ac81cdde4e02ce73a22080f
