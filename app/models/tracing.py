from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import db


class Tracing(db.Model):
    __tablename__ = "tracings"
    id = Column(Integer, primary_key=True)
    description = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer, ForeignKey("usuarios.id"))
    report_id = Column(Integer, ForeignKey("reports.id"))
    author = relationship("User", back_populates="tracings")
    report = relationship("Report", back_populates="tracings")
