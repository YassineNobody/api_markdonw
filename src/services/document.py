# src/services/document_service.py
from typing import Optional
from sqlalchemy.exc import IntegrityError
from src.extensions import db
from src.models.document import Document
from src.models.category import Category
from src.models.reference import Reference
from src.dto.document import (
    DocumentCreateRequest,
    DocumentIncludedResponse,
    DocumentUpdateRequest,  # <- DTO avec tous les champs optionnels
    DocumentResponse,
)
from src.errors import NotFoundError


class DocumentService:

    @staticmethod
    def _ensure_category_exists(category_id: int) -> None:
        if category_id is None:
            return
        if not Category.query.get(category_id):
            raise NotFoundError(f"Catégorie {category_id} introuvable.")

    @staticmethod
    def _ensure_reference_exists(reference_id: int) -> None:
        if reference_id is None:
            return
        if not Reference.query.get(reference_id):
            raise NotFoundError(f"Référence {reference_id} introuvable.")

    @staticmethod
    def create(data: DocumentCreateRequest) -> DocumentResponse:
        # validations relationnelles
        if data.category_id is not None:
            DocumentService._ensure_category_exists(data.category_id)
        if data.reference_id is not None:
            DocumentService._ensure_reference_exists(data.reference_id)

        doc = Document(
            title=data.title,  # type: ignore
            content=data.content,  # type: ignore
            category_id=data.category_id,  # type: ignore
            reference_id=data.reference_id,  # type: ignore
        )
        try:
            db.session.add(doc)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        return DocumentResponse.model_validate(doc)

    @staticmethod
    def get_by_id(document_id: int) -> DocumentResponse:
        doc = Document.query.get(document_id)
        if not doc:
            raise NotFoundError(f"Document {document_id} introuvable.")
        return DocumentResponse.model_validate(doc)

    @staticmethod
    def get_by_id_with_includes(document_id: int) -> DocumentIncludedResponse:
        doc = Document.query.get(document_id)
        if not doc:
            raise NotFoundError(f"Document {document_id} introuvable.")
        return DocumentIncludedResponse.model_validate(doc)

    @staticmethod
    def get_all() -> list[DocumentResponse]:
        docs = Document.query.all()
        return [DocumentResponse.model_validate(d) for d in docs]

    @staticmethod
    def list_all_with_includes() -> list[DocumentIncludedResponse]:
        docs = Document.query.all()
        return [DocumentIncludedResponse.model_validate(d) for d in docs]

    @staticmethod
    def update(document_id: int, data: DocumentUpdateRequest) -> DocumentResponse:
        doc = Document.query.get(document_id)
        if not doc:
            raise NotFoundError(f"Document {document_id} introuvable.")

        # validations relationnelles si on demande un changement
        if data.category_id is not None:
            DocumentService._ensure_category_exists(data.category_id)
        if data.reference_id is not None:
            DocumentService._ensure_reference_exists(data.reference_id)

        # mise à jour partielle (seulement champs fournis)
        if data.title is not None:
            doc.title = data.title
        if data.content is not None:
            doc.content = data.content
        if data.category_id is not None:
            doc.category_id = data.category_id
        if data.reference_id is not None:
            doc.reference_id = data.reference_id

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise
        except Exception:
            db.session.rollback()
            raise

        return DocumentResponse.model_validate(doc)

    @staticmethod
    def delete(document_id: int) -> None:
        doc = Document.query.get(document_id)
        if not doc:
            raise NotFoundError(f"Document {document_id} introuvable.")

        try:
            db.session.delete(doc)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def get_by_reference(reference_id: int) -> list[DocumentResponse]:
        docs = Document.query.filter_by(reference_id=reference_id).all()
        return [DocumentResponse.model_validate(d) for d in docs]

    @staticmethod
    def get_by_category(category_id: int) -> list[DocumentResponse]:
        docs = Document.query.filter_by(category_id=category_id).all()
        return [DocumentResponse.model_validate(d) for d in docs]

    @staticmethod
    def get_by_reference_includes(reference_id: int) -> list[DocumentIncludedResponse]:
        docs = Document.query.filter_by(reference_id=reference_id).all()
        return [DocumentIncludedResponse.model_validate(d) for d in docs]

    @staticmethod
    def get_by_category_includes(category_id: int) -> list[DocumentIncludedResponse]:
        docs = Document.query.filter_by(category_id=category_id).all()
        return [DocumentIncludedResponse.model_validate(d) for d in docs]
