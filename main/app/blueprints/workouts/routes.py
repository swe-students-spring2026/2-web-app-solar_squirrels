from flask import Blueprint, request, jsonify, render_template
from pydantic import ValidationError
from app.blueprints.workouts.service import WorkoutService


workouts_bp = Blueprint(
    "workouts",
    __name__,
    template_folder="templates",
    static_folder="static",
)

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

@workouts_bp.get("/list")
def workout_list_page(user_uuid):
    return render_template("workout_list.html", workouts=[], user_uuid=user_uuid)

@workouts_bp.get("/add")
def add_workout_page(user_uuid):
    return render_template("add_workout.html", user_uuid=user_uuid)

@workouts_bp.get("/<string:workout_uuid>")
def workout_detail_page(user_uuid, workout_uuid):
    workout = {
        "workout_uuid": workout_uuid,
        "date": "Feb 23, 2026",
        "date_str": "2026-02-23",
        "workout": {"type": "Strength", "duration": 45, "sets": [], "calories": 200},
    }
    return render_template("workout_detail.html", workout=workout, user_uuid=user_uuid)

@workouts_bp.get("/<string:workout_uuid>/edit")
def edit_workout_page(user_uuid, workout_uuid):
    workout = {
        "workout_uuid": workout_uuid,
        "date_str": "2026-02-23",
        "workout": {"type": "Strength", "duration": 45},
    }
    return render_template("edit_workout.html", workout=workout, user_uuid=user_uuid)

@workouts_bp.post("/<string:workout_uuid>/edit")
def edit_workout_submit(user_uuid, workout_uuid):
    return ("OK", 200)

@workouts_bp.post("/<string:workout_uuid>/delete")
def delete_workout_submit(user_uuid, workout_uuid):
    return ("OK", 200)

# ---------- TEMP PREVIEW ROUTES ----------

@workouts_bp.get("/ui/list")
def ui_workout_list(user_uuid):
    return render_template("workout_list.html", workouts=[], user_uuid=user_uuid)

@workouts_bp.get("/ui/add")
def ui_add_workout(user_uuid):
    return render_template("add_workout.html", user_uuid=user_uuid)

@workouts_bp.get("/ui/detail")
def ui_workout_detail(user_uuid):
    workout = {
        "workout_uuid": "1",
        "date": "Feb 23, 2026",
        "date_str": "2026-02-23",
        "workout": {
            "type": "Strength",
            "duration": 45,
            "sets": [],
            "calories": 200
        }
    }
    return render_template("workout_detail.html", workout=workout, user_uuid=user_uuid)

@workouts_bp.get("/ui/edit")
def ui_edit_workout(user_uuid):
    workout = {
        "workout_uuid": "1",
        "date_str": "2026-02-23",
        "workout": {
            "type": "Strength",
            "duration": 45
        }
    }
    return render_template("edit_workout.html", workout=workout, user_uuid=user_uuid)