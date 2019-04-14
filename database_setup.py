import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)

class Item(Base):
    __tablename__ = 'item'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    date_time = Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'title': self.title,
            'description': self.description,
            'id': self.id,
            'category_id': self.category_id,
            'date_time': self.date_time,
        }

engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)