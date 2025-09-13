# src/routes/category_routes.py
from flask import Blueprint, request, jsonify
from src.services.category import CategoryService
from src.dto.category import CategoryCreateRequest
from src.auth import require_api_token

category_bp = Blueprint("category", __name__, url_prefix="/categories")


@category_bp.route("/", methods=["POST"])
@require_api_token
def create_category():
    data = request.get_json()
    category_request = CategoryCreateRequest.model_validate(data)
    category_response = CategoryService.create(category_request)
    return jsonify(category_response.model_dump()), 201


@category_bp.route("/<int:category_id>", methods=["GET"])
def get_category(category_id):
    category_response = CategoryService.get_by_id(category_id)
    return jsonify(category_response.model_dump()), 200


@category_bp.route("/", methods=["GET"])
def list_categories():
    categories = CategoryService.list_all()
    return jsonify([cat.model_dump() for cat in categories]), 200


@category_bp.route("/<int:category_id>", methods=["DELETE"])
@require_api_token
def delete_category(category_id):
    CategoryService.delete(category_id)
    return "Catégorie supprimée avec succès.", 200
