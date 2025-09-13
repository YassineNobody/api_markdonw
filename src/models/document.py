from src.extensions import db
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

class Document(db.Model):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)

    # Relation vers Category
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    category = relationship("Category", back_populates="documents")

    # Relation vers Reference
    reference_id = Column(Integer, ForeignKey("references.id"), nullable=True)
    reference = relationship("Reference", back_populates="documents")
