# src/models/reference.py
from src.extensions import db
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship


class Reference(db.Model):
    __tablename__ = "references"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)  # Nom du livre / cours
    author = Column(String(100), nullable=True)  # Auteur ou Shaykh
    description = Column(Text, nullable=True)    

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    category = relationship("Category", back_populates="references")

    documents = relationship("Document", back_populates="reference")
