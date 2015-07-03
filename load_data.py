#
# load_data.py - Populate DB with sample data for the Catalog App.
#

import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category
from database_setup import Base
from database_setup import Item
from database_setup import User


engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# ===User File===
with open('data/users.json') as users_file:
    users_data = json.load(users_file)

# loop through users in the JSON file and add to DB
for user_json in users_data['users']:
    user = User(name=user_json['name'],
                email=user_json['email'],
                picture=user_json['picture'])
    session.add(user)
    session.commit()
    # get our user for later reference
    jc = session.query(User).filter_by(email=user_json['email']).one()


# ===Catalog File===
with open('data/catalog.json') as catalog_file:
    catalog_data = json.load(catalog_file)

# loop through categories in the JSON file and add to DB
for genre_json in catalog_data['genres']:
    # Genre
    genre = Category(name=genre_json['name'],
                     user_id=jc.id)
    session.add(genre)
    session.commit()
    category = session.query(Category).filter_by(name=genre_json['name']).one()
    # loop through items in the category and add to DB
    for book_json in genre_json['books']:
        # Book
        item = Item(category_id=category.id,
                    name=book_json['name'],
                    description=book_json['description'],
                    image_name=book_json['image_name'],
                    user_id=jc.id)
        session.add(item)
        session.commit()
