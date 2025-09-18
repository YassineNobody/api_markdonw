from flask import Blueprint, request, jsonify
from src.services.document import DocumentService
from src.dto.document import DocumentCreateRequest, DocumentUpdateRequest
from src.auth import require_api_token

document_bp = Blueprint("document", __name__, url_prefix="/documents")
document_bp.strict_slashes = False

@document_bp.route("", methods=["POST"])
@require_api_token
def create_document():
    data = request.get_json()
    document_request = DocumentCreateRequest.model_validate(data)
    document_response = DocumentService.create(document_request)
    return jsonify(document_response.model_dump()), 201


@document_bp.route("", methods=["GET"])
def list_documents():
    include = request.args.get("include", "false").lower() == "true"
    category_id = request.args.get("category_id", type=int)
    reference_id = request.args.get("reference_id", type=int)

    if category_id is not None:
        docs = (
            DocumentService.get_by_category_includes(category_id)
            if include
            else DocumentService.get_by_category(category_id)
        )
    elif reference_id is not None:
        docs = (
            DocumentService.get_by_reference_includes(reference_id)
            if include
            else DocumentService.get_by_reference(reference_id)
        )
    else:
        docs = (
            DocumentService.list_all_with_includes()
            if include
            else DocumentService.get_all()
        )

    return jsonify([doc.model_dump() for doc in docs]), 200


@document_bp.route("/<int:document_id>", methods=["GET"])
def get_document(document_id):
    include = request.args.get("include", "false").lower() == "true"
    if include:
        doc = DocumentService.get_by_id_with_includes(document_id)
    else:
        doc = DocumentService.get_by_id(document_id)
    return jsonify(doc.model_dump()), 200


@document_bp.route("/slug/<string:slug>", methods=["GET"])
def get_document_by_slug(slug):
    include = request.args.get("include", "false").lower() == "true"
    if include:
        doc = DocumentService.get_by_slug_with_includes(slug)
    else:
        doc = DocumentService.get_by_slug(slug)
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
