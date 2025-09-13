from flask import Blueprint, request, jsonify
from src.services.document import DocumentService
from src.dto.document import DocumentCreateRequest, DocumentUpdateRequest
from src.auth import require_api_token

document_bp = Blueprint("document", __name__, url_prefix="/documents")


@document_bp.route("/", methods=["POST"])
@require_api_token
def create_document():
    data = request.get_json()
    document_request = DocumentCreateRequest.model_validate(data)
    document_response = DocumentService.create(document_request)
    return jsonify(document_response.model_dump()), 201


@document_bp.route("/", methods=["GET"])
def list_documents():
    include = request.args.get("include", "false").lower() == "true"
    if include:
        docs = DocumentService.list_all_with_includes()
    else:
        docs = DocumentService.get_all()
    return jsonify([doc.model_dump() for doc in docs]), 200


@document_bp.route("/<int:document_id>", methods=["GET"])
def get_document(document_id):
    include = request.args.get("include", "false").lower() == "true"
    if include:
        doc = DocumentService.get_by_id_with_includes(document_id)
    else:
        doc = DocumentService.get_by_id(document_id)
    return jsonify(doc.model_dump()), 200


@document_bp.route("/<int:document_id>", methods=["PATCH"])
@require_api_token
def update_document(document_id):
    data = request.get_json()
    document_request = DocumentUpdateRequest.model_validate(data)
    document_response = DocumentService.update(document_id, document_request)
    return jsonify(document_response.model_dump()), 200


@document_bp.route("/<int:document_id>", methods=["DELETE"])
@require_api_token
def delete_document(document_id):
    DocumentService.delete(document_id)
    return jsonify({"message": f"Document {document_id} supprimé"}), 200
