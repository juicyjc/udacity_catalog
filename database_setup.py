#
# database_setup.py - Database ORM and database creation for the Catalog App.
#

import datetime

from flask import url_for

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import UniqueConstraint

from xml.etree import ElementTree as ET

from werkzeug.contrib.atom import AtomFeed

from urlparse import urljoin

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False)
    picture = Column(String(80))

    @property
    def serialize(self):
        """Return User object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'email': self.email,
            'picture': self.picture,
        }

    @classmethod
    # === Return XML object of all users. ===
    def getUsersXML(cls, session, root):
        """
        ####Args####
            - session:  the DB session
            - root:  the root XML node

        ####Returns####
            - root:  the populated root XML node
        """
        users = session.query(User).order_by(User.name.asc())
        for user in users:
            userNode = ET.SubElement(root, 'user')
            name = ET.SubElement(userNode, 'name')
            name.text = user.name
            id = ET.SubElement(userNode, 'id')
            id.text = str(user.id)
            email = ET.SubElement(userNode, 'email')
            email.text = user.email
            picture = ET.SubElement(userNode, 'picture')
            picture.text = user.picture
        return root


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    items = relationship("Item", backref="category",
                         cascade="all, delete, delete-orphan")
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serializePartial(self):
        """Return Category object data without items"""
        return {
            'name': self.name,
            'id': self.id,
            'created_by': self.user.name
        }

    @property
    def serialize(self):
        """Return Category object data in easily serializeable format"""
        items = [i.serialize for i in self.items]
        return {
            'name': self.name,
            'id': self.id,
            'books': items,
            'created_by': self.user.name
        }

    @classmethod
    # === Return XML object of a category. ===
    def getCategoryXML(cls, session, category_id, root):
        """
        ####Args####
            - session:  the DB session
            - category_id:  id of the category
            - root:  the root XML node

        ####Returns####
            - root:  the populated root XML node
        """
        category = session.query(Category).filter_by(id=category_id).one()
        items = session.query(Item).filter_by(
                category_id=category.id).order_by(Item.name.asc())
        name = ET.SubElement(root, 'name')
        name.text = category.name
        id = ET.SubElement(root, 'id')
        id.text = str(category.id)
        user = ET.SubElement(root, 'created_by')
        user.text = str(category.user.name)
        books = ET.SubElement(root, 'books')
        for item in items:
            book = ET.SubElement(books, 'book')
            Item.getItemXML(session, item.id, book)
        return root

    @classmethod
    # === Return XML object of the catalog. ===
    def getCatalogXML(cls, session, root):
        """
        ####Args####
            - session:  the DB session
            - root:  the root XML node

        ####Returns####
            - root:  the populated root XML node
        """
        categories = session.query(Category).order_by(Category.name.asc())
        for category in categories:
            genre = ET.SubElement(root, 'genre')
            Category.getCategoryXML(session, category.id, genre)
        return root


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
        # Returns Item object data in easily serializeable format
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

    @classmethod
    # === Return XML object of a book. ===
    def getItemXML(cls, session, item_id, root):
        """
        ####Args####
            - session:  the DB session
            - item_id:  id of the book
            - root:  the root XML node

        ####Returns####
            - root:  the populated root XML node
        """
        item = session.query(Item).filter_by(id=item_id).one()
        name = ET.SubElement(root, 'name')
        name.text = item.name
        description = ET.SubElement(root, 'description')
        description.text = item.description
        id = ET.SubElement(root, 'id')
        id.text = str(item.id)
        category = ET.SubElement(root, 'genre')
        category.text = str(item.category.name)
        user = ET.SubElement(root, 'created_by')
        user.text = str(item.user.name)
        date_added = ET.SubElement(root, 'date_added')
        date_added.text = str(item.date_added)
        date_modified = ET.SubElement(root, 'date_modified')
        date_modified.text = str(item.date_modified)
        image_name = ET.SubElement(root, 'image_name')
        image_name.text = str(item.image_name)
        return root

    @classmethod
    # === Return Atoms feed object of recently added/modified books. ===
    def getRecentItemsAtom(cls, session, name, feed_url, url):
        """
        ####Args####
            - session:  the DB session
            - name:  the name of the feed
            - feed_url:  URL that dispalys the Atom feed
            - url:  root URL

        ####Returns####
            - feed:  the populated Atom feed
        """
        feed = AtomFeed(name, feed_url=feed_url, url=url)
        items = session.query(Item).order_by(
            Item.date_modified.desc()).limit(10)
        for item in items:
            feed.add(item.name, item.description,
                     content_type='html',
                     user=item.user.name,
                     url=urljoin(
                        url,
                        url_for('showItem',
                                category_id=item.category.id,
                                item_id=item.id)),
                     updated=item.date_modified,
                     published=item.date_added)
        return feed


engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
