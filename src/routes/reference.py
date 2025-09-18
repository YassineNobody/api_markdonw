from flask import Blueprint, request, jsonify
from src.dto.reference import ReferenceCreateRequest
from src.services.reference import ReferenceService
from src.auth import require_api_token

reference_bp = Blueprint("reference", __name__, url_prefix="/references")
reference_bp.strict_slashes = False

@reference_bp.route("", methods=["POST"])
@require_api_token
def create_reference():
    data = request.get_json()
    reference_request = ReferenceCreateRequest.model_validate(data)
    reference_response = ReferenceService.create(reference_request)
    return jsonify(reference_response.model_dump()), 201


@reference_bp.route("/<int:reference_id>", methods=["GET"])
def get_reference(reference_id):
    reference_response = ReferenceService.get_by_id(reference_id)
    return jsonify(reference_response.model_dump()), 200


@reference_bp.route("/slug/<string:slug>", methods=["GET"])
def get_reference_by_slug(slug):
    reference_response = ReferenceService.get_by_slug(slug)
    return jsonify(reference_response.model_dump()), 200


@reference_bp.route("", methods=["GET"])
def list_references():
    references = ReferenceService.list_all()
    return jsonify([ref.model_dump() for ref in references]), 200


@reference_bp.route("/<int:reference_id>", methods=["DELETE"])
@require_api_token
def delete_reference(reference_id):
    ReferenceService.delete(reference_id)
    return jsonify({"message": "Référence supprimée avec succès."}), 200
