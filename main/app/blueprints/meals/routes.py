from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from datetime import datetime

from app.blueprints.meals.service import MealService
from app.blueprints.meals.models import MealEntry

meals_bp = Blueprint("meals", __name__)


@meals_bp.route("/<string:user_id>", methods=["GET"])
def get_user_meals(user_id):
    try:
        date_str = request.args.get("date")
        if not date_str:
            return jsonify({"error": "Date parameter is required"}), 400
        
        date = datetime.fromisoformat(date_str)
        meals = MealService.get_user_meals(user_id, date)
        return jsonify(meals.model_dump()), 200
    
    except ValueError as e:
        return jsonify({"error": "Invalid date format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@meals_bp.route("/<string:user_id>", methods=["POST"])
def add_meal(user_id):
    try:
        date_str = request.json.get("date")
        if not date_str:
            return jsonify({"error": "Date is required"}), 400
        
        date = datetime.fromisoformat(date_str)
        meal_entry = MealEntry(**request.json.get("meal_entry"))
        
        updated_meals = MealService.update_meals(user_id, date, meal_entry)
        return jsonify(updated_meals.model_dump()), 201
    
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": "Invalid date format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
