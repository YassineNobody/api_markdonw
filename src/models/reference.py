from src.extensions import db
from sqlalchemy import Column, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship


class Reference(db.Model):
    __tablename__ = "references"
    __table_args__ = (UniqueConstraint("title", "author", name="uq_title_author"),)

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)

    documents = relationship("Document", back_populates="reference")
