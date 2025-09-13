from src.extensions import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Category(db.Model):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)

    # Relation inverse vers Document
    documents = relationship("Document", back_populates="category")
