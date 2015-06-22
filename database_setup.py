#
# database_setup.py - database ORM and creation for the Catalog App
#

import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False)
    picture = Column(String(80))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'email': self.email,
            'picture': self.picture,
        }


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    items = relationship("Item", backref="category",
                         cascade="all, delete, delete-orphan")
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serializePartial(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'created_by': self.user.name
        }

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        items = [i.serialize for i in self.items]
        return {
            'name': self.name,
            'id': self.id,
            'books': items,
            'created_by': self.user.name
        }


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    image_name = Column(String(80))
    date_added = Column(DateTime(timezone=False),
                        default=datetime.datetime.utcnow)
    date_modified = Column(DateTime(timezone=False),
                           default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.utcnow)
    category_id = Column(Integer, ForeignKey('category.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        # Returns object data in easily serializeable format
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'date_added': self.date_added,
            'date_modified': self.date_modified,
            'genre': self.category.name,
            'created_by': self.user.name,
            'image_name': self.image_name
        }

engine = create_engine('sqlite:///catalog.db')


Base.metadata.create_all(engine)
