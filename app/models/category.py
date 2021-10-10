from sqlalchemy import Column, Integer, String
from app.db import db

class Category(db.Model):

    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)

    def __init__(self, name=None):
        self.name = name