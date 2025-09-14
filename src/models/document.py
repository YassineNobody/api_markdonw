from src.extensions import db
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, validates
from slugify import slugify


class Document(db.Model):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    # Relation vers Category
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    category = relationship("Category", back_populates="documents")

    # Relation vers Reference
    reference_id = Column(Integer, ForeignKey("references.id"), nullable=True)
    reference = relationship("Reference", back_populates="documents")

    @validates("title", "reference_id")
    def generate_slug(self, key, value):
        """
        Construit un slug basé sur :
        - le slug de la référence (si présente)
        - le titre du document
        """
        title = value if key == "title" else self.title
        reference_id = value if key == "reference_id" else self.reference_id

        base_slug = slugify(str(title))

        if reference_id is not None:
            ref = db.session.get(
                self.__class__.reference.property.mapper.class_, reference_id
            )
            if ref and ref.slug:
                self.slug = f"{ref.slug}-{base_slug}"
            else:
                self.slug = base_slug
        else:
            self.slug = base_slug

        return value
