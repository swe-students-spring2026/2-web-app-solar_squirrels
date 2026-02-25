from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from datetime import datetime

from app.blueprints.water.service import WaterService
from app.blueprints.water.models import WaterItem

water_bp = Blueprint("water", __name__)


@water_bp.route("/<string:user_id>", methods=["GET"])
def get_user_water(user_id):
    try:
        date_str = request.args.get("date")
        if not date_str:
            return jsonify({"error": "Date parameter is required"}), 400
        
        date = datetime.fromisoformat(date_str)
        water = WaterService.get_user_water(user_id, date)
        return jsonify(water.model_dump()), 200
    
    except ValueError as e:
        return jsonify({"error": "Invalid date format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@water_bp.route("/<string:user_id>", methods=["POST"])
def add_water(user_id):
    try:
        date_str = request.json.get("date")
        if not date_str:
            return jsonify({"error": "Date is required"}), 400
        
        date = datetime.fromisoformat(date_str)
        water_item = WaterItem(**request.json.get("water_item"))
        
        updated_water = WaterService.update_water(user_id, date, water_item)
        return jsonify(updated_water.model_dump()), 201
    
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": "Invalid date format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
