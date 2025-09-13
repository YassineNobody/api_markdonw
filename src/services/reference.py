from src.extensions import db
from src.models.reference import Reference
from src.dto.reference import ReferenceCreateRequest, ReferenceResponse
from src.errors import ConflictError, NotFoundError


class ReferenceService:

    @staticmethod
    def create(data: ReferenceCreateRequest) -> ReferenceResponse:
        existing = Reference.query.filter_by(
            title=data.title, author=data.author
        ).first()
        if existing:
            raise ConflictError(
                f"La référence '{data.title}' de '{data.author}' existe déjà."
            )

        reference = Reference(
            title=data.title,  # type: ignore
            author=data.author,  # type: ignore
            description=data.description,  # type: ignore
        )
        db.session.add(reference)
        db.session.commit()

        return ReferenceResponse.model_validate(reference)

    @staticmethod
    def list_all() -> list[ReferenceResponse]:
        refs = Reference.query.all()
        return [ReferenceResponse.model_validate(r) for r in refs]

    @staticmethod
    def get_by_id(reference_id: int) -> ReferenceResponse:
        ref = Reference.query.get(reference_id)
        if not ref:
            raise NotFoundError(f"Référence {reference_id} introuvable.")
        return ReferenceResponse.model_validate(ref)

    @staticmethod
    def delete(reference_id: int) -> None:
        ref = Reference.query.get(reference_id)
        if not ref:
            raise NotFoundError(f"Référence {reference_id} introuvable.")

        db.session.delete(ref)
        db.session.commit()