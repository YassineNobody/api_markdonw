from src.extensions import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, validates
from slugify import slugify

class Category(db.Model):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    slug = Column(String(255), nullable=False, unique=True)

    references = relationship(
        "Reference",
        back_populates="category",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    documents = relationship(
        "Document",
        back_populates="category",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    @validates("name")
    def generate_slug(self, key, value):
        self.slug = slugify(value)
        return value
