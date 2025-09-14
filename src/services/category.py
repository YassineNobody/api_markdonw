from src.dto.reference import ReferenceResponse
from src.errors import ConflictError, NotFoundError
from src.extensions import db
from src.models.category import Category
from src.dto.category import (
    CategoryCreateRequest,
    CategoryIncludeReferencesResponse,
    CategoryResponse,
)


class CategoryService:

    @staticmethod
    def create(data: CategoryCreateRequest) -> CategoryResponse:
        existing = Category.query.filter_by(name=data.name).first()
        if existing:
            raise ConflictError(f"La catégorie '{data.name}' existe déjà.")

        category = Category(name=data.name, description=data.description)  # type: ignore
        db.session.add(category)
        db.session.commit()
        return CategoryResponse.model_validate(category)

    @staticmethod
    def get_by_id(category_id: int) -> CategoryResponse:
        category = Category.query.get(category_id)
        if not category:
            raise NotFoundError(f"Catégorie {category_id} introuvable.")
        return CategoryResponse.model_validate(category)

    @staticmethod
    def list_all() -> list[CategoryResponse]:
        categories = Category.query.all()
        return [CategoryResponse.model_validate(cat) for cat in categories]

    @staticmethod
    def delete(category_id: int) -> None:
        category = Category.query.get(category_id)
        if not category:
            raise NotFoundError(f"Catégorie {category_id} introuvable.")

        db.session.delete(category)
        db.session.commit()

    @staticmethod
    def get_references(category_id: int) -> list[ReferenceResponse]:
        category = Category.query.get(category_id)
        if not category:
            raise NotFoundError(f"Catégorie {category_id} introuvable.")

        return [ReferenceResponse.model_validate(ref) for ref in category.references]

    @staticmethod
    def get_categories_with_references() -> list[CategoryIncludeReferencesResponse]:
        categories = Category.query.all()
        return [
            CategoryIncludeReferencesResponse.model_validate(cat)
            for cat in categories
            if cat.references
        ]

    @staticmethod
    def get_by_id_with_references(
        category_id: int,
    ) -> CategoryIncludeReferencesResponse:
        category = Category.query.get(category_id)
        if not category:
            raise NotFoundError(f"Catégorie {category_id} introuvable.")
        return CategoryIncludeReferencesResponse.model_validate(category)
