#
# utils.py - Utilities and database helpers for application.py.
#

import os

from database_setup import Category
from database_setup import Item
from database_setup import User

from flask import url_for
from flask import flash

from werkzeug import secure_filename

DEFAULT_THEME = 'cyborg'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             "static", "img",)


# === Check to see if file is of an allowed type and format. ===
def allowed_file(filename):
    """
    ####Args####
        + filename:  the filename to check

    ####Returns####
        + boolean - is the filename an allowed type and correct format?
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# === Get the correct path to a book image. ===
def getImagePath(image_name):
    """
    ####Args####
        + image_name:  the name of the book

    ####Returns####
        + the relative path of the image
    """
    return os.path.join(UPLOAD_FOLDER, image_name)


# === Create the list of categories and add to session variables. ===
def setCategories(session, login_session):
    """
    ####Args####
        + session:  the DB session
        + login_session:  session variables

    ####Session Variables####
        + login_session['categories']:  list of category names
        + login_session['cat_num']:  number of categories
    """
    categories = session.query(Category).order_by(Category.name.asc())
    cat_num = session.query(Category).count()
    login_session['categories'] = [c.serializePartial for c in categories]
    login_session['cat_num'] = cat_num


# === Add the selected theme css URL to the session. ===
def setTheme(login_session, theme_name):
    """
    ####Args####
        + theme_name:  the name of the selected theme

    ####Session Variables####
        + login_session['theme_url']:  URL of the selected Bootstrap css theme
    """
    theme_filename = 'css/bootstrap_{}.min.css'.format(theme_name)
    login_session['theme_url'] = url_for('static', filename=theme_filename)


# === Set the categories and theme URL session variables if not set. ===
def setDefaults(session, login_session):
    """
    ####Args####
        + session:  the DB session
        + login_session:  session variables
    """
    if 'categories' not in login_session or 'cat_num' not in login_session:
        setCategories(session, login_session)
    if 'theme_url' not in login_session:
        setTheme(login_session, DEFAULT_THEME)


# === Create a new user. ===
def createUser(session, login_session):
    """
    ####Args####
        + session:  the DB session
        + login_session:  session variables

    ####Returns####
        + user.id:  id of the new user
    """
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# === Get a user object. ===
def getUserInfo(session, user_id):
    """
    ####Args####
        + session:  the DB session
        + user_id:  id of the user to retrieve

    ####Returns####
        + user:  the user object
    """
    user = session.query(User).filter_by(id=user_id).one()
    return user


# === Get user id from email address. ===
def getUserID(session, email):
    """
    ####Args####
        + session:  the DB session
        + email:  email address of the user

    ####Returns####
        + user.id:  the user id
    """
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# === Get user and creator information. ===
def getCreatorInfo(session, login_session, creator_id):
    """
    ####Args####
        + session:  the DB session
        + login_session:  session variables
        + creator_id:  the user_id of the object creator

    ####Returns####
        + creator_info['logged_in']:  boolean - is the user logged in?
        + creator_info['is_creator']:  boolean - is user_id == creator_id?
    """
    creator = getUserInfo(session, creator_id)
    logged_in = False
    is_creator = False
    if 'username' in login_session:
        logged_in = True
        if creator.id == login_session['user_id']:
            is_creator = True
    return dict([('logged_in', logged_in), ('is_creator', is_creator)])


# === Redirect if user is not creator. ===
def creatorCheck(login_session, creator_id, obj_type, crud_type):
    """
    ####Args####
        + login_session:  session variables
        + creator_id:  the user_id of the object creator
        + obj_type:  string - text - 'genres' or 'books'
        + crud_type:  string - text - 'delete' or 'edit'

    ####Returns####
        + boolean - is the user the creator of the object
    """
    # If not the author of this object, return false
    if creator_id != login_session['user_id']:
        flash('You can only {} your own {}.'.format(crud_type, obj_type),
              'error')
        return False
    return True


# === Create new category. ===
def createGenre(session, login_session, name, user_id):
    """
    ####Args####
        + session:  the DB session
        + login_session:  session variables
        + name:  name of the new genre
        + user_id:  the user_id of the creator
    ####Returns####
        + category_id - id of the newly created genre
    """
    try:
        newCategory = Category(name=name, user_id=user_id)
        session.add(newCategory)
        session.commit()
        category = session.query(Category).filter_by(name=name).one()
        setCategories(session, login_session)
        flash("New Genre Created")
        return category.id
    except:
        session.rollback()
        flash("Genre Already Exists", 'error')


# === Edit a category. ===
def updateGenre(session, login_session, category, name):
    """
    ####Args####
        + session:  the DB session
        + login_session:  session variables
        + category:  the category object to update
        + name:  name of the genre
    """
    try:
        if name:
            category.name = name
        session.add(category)
        session.commit()
        setCategories(session, login_session)
        flash("Genre Successfully Edited")
    except:
        session.rollback()
        flash("Genre Already Exists", 'error')


# === Delete a category. ===
def deleteGenre(session, login_session, category):
    """
    ####Args####
        + session:  the DB session
        + login_session:  session variables
        + category:  the category object to delete
    """
    # first delete all of the books in the category
    deleteBooks(session, category.id)
    session.delete(category)
    session.commit()
    setCategories(session, login_session)
    flash("Genre Successfully Deleted")


# === Create an item. ===
def createBook(session, image, category_id, name, description, user_id):
    """
    ####Args####
        + session:  the DB session
        + image:  the image file from the form
        + category_id:  the id of the category the book belongs to
        + name:  name of the new genre
        + description:  a full description of the book
        + user_id:  the user_id of the creator

    ####Returns####
        + item_id - id of the newly created book
    """
    image_name = None
    if image and allowed_file(image.filename):
        image_name = secure_filename(image.filename)
        image.save(getImagePath(image_name))
    newItem = Item(category_id=category_id,
                   name=name,
                   description=description,
                   image_name=image_name,
                   user_id=user_id)
    session.add(newItem)
    session.commit()
    item = session.query(Item).filter_by(name=name).one()
    flash("New Book Created")
    return item.id


# === Edit an item. ===
def updateBook(session, item, image, category_id, name, description):
    """
    ####Args####
        + session:  the DB session
        + item:  the item object to update
        + image:  the image file from the form
        + category_id:  the id of the category the book belongs to
        + name:  name of the new genre
        + description:  a full description of the book
    """
    if name:
        item.name = name
    if category_id:
        item.category_id = category_id
    if description:
        item.description = description
    if image and allowed_file(image.filename):
        new_image_name = secure_filename(image.filename)
        # If the new image name is not the same as the old
        if item.image_name != new_image_name:
            # Delete the old image
            if item.image_name is not None:
                os.remove(getImagePath(item.image_name))
            # Set the new image name
            item.image_name = new_image_name
            # Save the new image
            image.save(getImagePath(item.image_name))
    session.add(item)
    session.commit()
    flash("Book Successfully Edited")


# === Delete an item. ===
def deleteBook(session, item, display_flash):
    """
    ####Args####
        + session:  the DB session
        + item:  the item object to delete
        + display_flash:  boolean - display flash message after delete
    """
    if item.image_name is not None:
        os.remove(getImagePath(item.image_name))
    session.delete(item)
    session.commit()
    if display_flash:
        flash("Book Successfully Deleted")


# === Delete all items from a category. ===
def deleteBooks(session, category_id):
    """
    ####Args####
        + session:  the DB session
        + category_id:  the id of the category to delete
    """
    items = session.query(Item).filter_by(category_id=category_id)
    for item in items:
        deleteBook(session, item, False)
