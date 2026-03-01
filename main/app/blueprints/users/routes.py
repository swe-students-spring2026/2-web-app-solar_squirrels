from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from app.blueprints.users.service import UserService

users_bp = Blueprint("users", __name__)

@users_bp.route("/", methods=["GET"])
def get_all_users():
    users = UserService.get_all_users()
    return jsonify(users), 200


@users_bp.route("/<string:uuid>", methods=["GET"])
def get_user(uuid):
    user = UserService.get_user_by_uuid(uuid)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user), 200


@users_bp.route("/", methods=["POST"])
def create_user():
    try:
        user = UserService.create_user(request.json)
        return jsonify(user), 201

    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

@users_bp.route("/<string:uuid>", methods=["PUT"])
def complete_profile(uuid):
    try:
        updated_user = UserService.update_user(uuid, request.json)

        if not updated_user:
            return jsonify({"error": "User not found"}), 404

        return jsonify(updated_user), 200

    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400


@users_bp.route("/<string:uuid>", methods=["DELETE"])
def delete_user(uuid):
    deleted = UserService.delete_user(uuid)

    if not deleted:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User deleted successfully"}), 200