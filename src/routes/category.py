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
    include = request.args.get("include", "false").lower() == "true"

    if include:
        category_response = CategoryService.get_by_id_with_references(category_id)
    else:
        category_response = CategoryService.get_by_id(category_id)

    return jsonify(category_response.model_dump()), 200


@category_bp.route("/slug/<string:slug>", methods=["GET"])
def get_category_by_slug(slug):
    include = request.args.get("include", "false").lower() == "true"
    category_response = CategoryService.get_by_slug(slug, include_ref=include)
    return jsonify(category_response.model_dump()), 200


@category_bp.route("/", methods=["GET"])
def list_categories():
    include = request.args.get("include", "false").lower() == "true"

    if include:
        categories = CategoryService.get_categories_with_references()
    else:
        categories = CategoryService.list_all()

    return jsonify([cat.model_dump() for cat in categories]), 200


@category_bp.route("/<int:category_id>", methods=["DELETE"])
@require_api_token
def delete_category(category_id):
    CategoryService.delete(category_id)
    return jsonify({"message": "Catégorie supprimée avec succès."}), 200
