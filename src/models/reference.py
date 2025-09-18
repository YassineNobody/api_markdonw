from src.extensions import db
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, validates
from slugify import slugify


class Reference(db.Model):
    __tablename__ = "references"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)  # Nom du livre / cours
    author = Column(String(100), nullable=True)  # Auteur ou Shaykh
    slug = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)

    category_id = Column(
        Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=True
    )
    category = relationship("Category", back_populates="references")
    documents = relationship(
        "Document",
        back_populates="reference",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    @validates("title", "author")
    def generate_slug(self, key, value):
        # Récupère la valeur finale pour title et author
        title = value if key == "title" else self.title
        author = value if key == "author" else self.author

        if author is not None and author.strip():
            self.slug = slugify(f"{title}-{author}")
        else:
            self.slug = slugify(str(title))

        return value
