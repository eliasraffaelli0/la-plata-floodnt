from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import db


class Report(db.Model):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=True)
    category = Column(String(50))
    description = Column(String(500))
    latitude = Column(String(50), unique=True)
    longitude = Column(String(50), unique=True)
    state = Column(String(50))
    complainant_telephone = Column(String(50))
    complainant_email = Column(String(50))
    complainant_name = Column(String(50))
    complainant_last_name = Column(String(50))
    closed_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("usuarios.id"))
    assigned_to = relationship("User", back_populates="reports")
    tracings = relationship("Tracing", back_populates="report")
