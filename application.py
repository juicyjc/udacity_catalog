#
# appliction.py - Webserver and code for the Catalog App.
#

import random
import string
import httplib2
import json
import requests
import utils

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import jsonify
from flask import make_response
from flask import session as login_session

from flask.ext.seasurf import SeaSurf

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import AccessTokenCredentials

from database_setup import Category
from database_setup import Base
from database_setup import Item
from database_setup import User

from xml.etree import ElementTree as ET

from functools import wraps


app = Flask(__name__)
csrf = SeaSurf(app)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"

READ_FOLDER = '/static/img/'

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# === Login decorator. ===
def loginRequired(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            return redirect(url_for('showLogin', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# === Create anti-forgery state token. ===
@csrf.exempt
@app.route('/login')
def showLogin():
    """
    ####Returns####
        + Template:  login.html
        + STATE:  the state token
    """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# ===  Login with Facebook. ===
@csrf.exempt
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.2/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.2/me?%s' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    # set the session variables
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly
    # logout, let's strip out the information before the equals sign in
    # our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.2/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = utils.getUserID(session, login_session['email'])
    if not user_id:
        user_id = utils.createUser(session, login_session)
    login_session['user_id'] = user_id

    flash("Now logged in as %s." % login_session['username'])
    return "success"


# === Disconnect from Facebook. ===
@csrf.exempt
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must be included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?fb_exchange_token=%s' % (
        facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "success"


# === Login with Google. ===
@csrf.exempt
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
                     json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    # set the session variables
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = utils.getUserID(session, login_session['email'])
    if not user_id:
        user_id = utils.createUser(session, login_session)
    login_session['user_id'] = user_id

    flash("You are now logged in as %s." % login_session['username'])
    return 'success'


# === Disconnect from Google. ===
@csrf.exempt
@app.route('/gdisconnect')
def gdisconnect():
    """
    Revoke a current user's token and reset their login_session.
    """
    # Only disconnect a connected user.
    credentials = AccessTokenCredentials(login_session['credentials'],
                                         'user-agent-value')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# === Disconnect based on provider. ===
@csrf.exempt
@app.route('/disconnect')
def disconnect():
    """
    ####Returns####
        + redirect:  showCatalog
    """
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCatalog'))
    else:
        flash("You were not logged in.")
        return redirect(url_for('showCatalog'))


# === Set the Bootstrap theme based on the user's selection. ===
@app.route('/theme/<theme_name>')
def theme(theme_name):
    """
    ####Args####
        + theme_name:  the name of the theme selected by the user

    ####Returns####
        + redirect:  showCatalog
    """
    utils.setTheme(login_session, theme_name)
    return redirect(url_for('showCatalog'))


# === Display the catalog - genres and books. ===
@app.route('/')
@app.route('/catalog')
def showCatalog():
    """
    ####Returns####
        + template:  catalog.html
        + items:  a list of recent books
        + item_num:  the nuber of books
        + logged_in:  boolean
    """
    utils.setDefaults(session, login_session)
    items = session.query(Item).order_by(Item.date_modified.desc()).limit(10)
    item_num = session.query(Item).order_by(
                Item.date_modified.desc()).limit(10).count()
    logged_in = False
    if 'username' in login_session:
        logged_in = True
    return render_template('catalog.html', items=items,
                           item_num=item_num, logged_in=logged_in)


# === Display the items in the selected category. ===
@app.route('/catalog/<int:category_id>/items')
def showItems(category_id):
    """
    ####Args####
        + category_name:  the category that we're displaying

    ####Returns####
        + template:  items.html
        + items:  the books in this category
        + item_num:  the number of books
        + category_name:  the selected category
        + category_id:  the id of the selected category
        + logged_in:  boolean
        + is_creator:  boolean
    """
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(
              category_id=category.id).order_by(Item.name.asc())
    item_num = session.query(Item).filter_by(category_id=category.id).count()
    creator_info = utils.getCreatorInfo(
        session, login_session, category.user_id)
    return render_template('items.html', items=items, item_num=item_num,
                           category_name=category.name,
                           category_id=category.id,
                           logged_in=creator_info['logged_in'],
                           is_creator=creator_info['is_creator'])


# === Create a new Category. ===
@app.route('/catalog/category/new', methods=['GET', 'POST'])
@loginRequired
def newCategory():
    """
    ####Returns####
    #####GET#####
        + template:  newCategory.html
    #####POST#####
        + redirect:  showItems
        + category_id - the id of the newly created category
    """
    if request.method == 'POST':
        category_id = utils.createGenre(session, login_session,
                                        request.form['name'],
                                        login_session['user_id'])
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('newCategory.html')


# === Edit a Category. ===
@app.route('/catalog/<int:category_id>/edit', methods=['GET', 'POST'])
@loginRequired
def editCategory(category_id):
    """
    ####Args####
        + category_id:  the id of the category that we're editing

    ####Returns####
    #####GET#####
        + template:  editCategory.html
        + category - the category object
    #####POST#####
        + redirect:  showItems
        + category_id - the id of the category we're editing
    """
    category = session.query(Category).filter_by(id=category_id).one()
    if not utils.creatorCheck(login_session, category.user_id,
                              'genres', 'edit'):
        return redirect('/')
    if request.method == 'POST':
        utils.updateGenre(session, login_session,
                          category, request.form['name'])
        return redirect(url_for('showItems', category_id=category.id))
    else:
        return render_template('editCategory.html', category=category)


# === Delete a Category. ===
@app.route('/catalog/<int:category_id>/delete', methods=['GET', 'POST'])
@loginRequired
def deleteCategory(category_id):
    """
    ####Args####
    + category_id:  the id of the category that we're deleting

    ####Returns####
    #####GET#####
        + template:  deleteCategory.html
        + category - the category object
    #####POST#####
        + redirect:  showCatalog
    """
    category = session.query(Category).filter_by(id=category_id).one()
    if not utils.creatorCheck(login_session, category.user_id,
                              'genres', 'delete'):
        return redirect('/')
    if request.method == 'POST':
        utils.deleteGenre(session, login_session, category)
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deleteCategory.html', category=category)


# === Display a book. ===
@app.route('/catalog/<int:category_id>/<int:item_id>')
def showItem(category_id, item_id):
    """
    ####Args####
        + category_id:  the id of the category that we're displaying
        + item_id:  the id of the item that we're displaying

    ####Returns####
        + template:  item.html
        + item - the item object
        + image_path - path to the item's image
        + logged_in - boolean
        + is_creator - boolean
    """
    item = session.query(Item).filter_by(id=item_id).one()
    image_path = None
    if item.image_name is not None:
        image_path = READ_FOLDER + item.image_name
    creator_info = utils.getCreatorInfo(session, login_session, item.user_id)
    return render_template('item.html', item=item, image_path=image_path,
                           logged_in=creator_info['logged_in'],
                           is_creator=creator_info['is_creator'])


# === Create a book. ===
@app.route('/catalog/item/new', methods=['GET', 'POST'])
@loginRequired
def newItem():
    """
    ####Returns####
    #####GET#####
        + template:  newItem.html
        + category_name - the name of the category of the new book
    #####POST#####
        + redirect:  showItems
        + category_id - the category id of the new book
    """
    if request.method == 'POST':
        item_id = utils.createBook(session, request.files['image'],
                                   request.form['category_id'],
                                   request.form['name'],
                                   request.form['description'],
                                   login_session['user_id'])
        return redirect(url_for('showItems', category_id=request.form['category_id']))
    else:
        category_name = request.args.get('category_name')
        return render_template('newItem.html', category_name=category_name)


# === Edit a book. ===
@app.route('/catalog/<int:category_id>/<int:item_id>/edit', methods=['GET', 'POST'])
@loginRequired
def editItem(category_id, item_id):
    """
    ####Args####
        + category_id:  the id of the category of the book that we're editing
        + item_id:  the id of the item that we're editing

    ####Returns####
    #####GET#####
        + template:  editItem.html
        + item - the item object
    #####POST#####
        + redirect:  showItems
        + category_id - the id of the category of the book
    """
    item = session.query(Item).filter_by(id=item_id).one()
    if not utils.creatorCheck(login_session, item.user_id, 'books', 'edit'):
        return redirect('/')
    if request.method == 'POST':
        utils.updateBook(session, item,
                         request.files['image'],
                         request.form['category_id'],
                         request.form['name'],
                         request.form['description'])
        return redirect(url_for('showItems', category_id=request.form['category_id']))
    else:
        return render_template('editItem.html', item=item)


# === Delete a book. ===
@app.route('/catalog/<int:category_id>/<int:item_id>/delete', methods=['GET', 'POST'])
@loginRequired
def deleteItem(category_id, item_id):
    """
    ####Args####
        + category_id:  the id of the category of the book that we're deleting
        + item_id:  the id of the item that we're deleting

    ####Returns####
    #####GET#####
        + template:  deleteItem.html
        + item - the item object
    #####POST#####
        + redirect:  showItems
        + category_id - the id of the category of the book
    """
    item = session.query(Item).filter_by(id=item_id).one()
    if not utils.creatorCheck(login_session, item.user_id, 'books', 'delete'):
        return redirect('/')
    if request.method == 'POST':
        utils.deleteBook(session, item, True)
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('deleteItem.html', item=item)


# === Return the catalog JSON object. ===
@app.route('/catalog.json')
def catalogJSON():
    """
    ####Returns####
        + genres:  JSON object of all genres and books
    """
    categories = session.query(Category).order_by(Category.name.asc())
    return jsonify(genres=[c.serialize for c in categories])


# === Return a category JSON object. ===
@app.route('/catalog/<int:category_id>/category.json')
def categoryJSON(category_id):
    """
    ####Args####
        + category_id:  the id of the category of the book

    ####Returns####
        + genre:  JSON object of the genre
    """
    category = session.query(Category).filter_by(id=category_id).one()
    return jsonify(genre=category.serialize)


# === Return a book JSON object. ===
@app.route('/catalog/<int:category_id>/<int:item_id>/item.json')
def itemJSON(category_id, item_id):
    """
    ####Args####
        + category_id:  the id of the category of the book
        + item_id:  the id of the book

    ####Returns####
        + book:  JSON object of the book
    """
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(book=item.serialize)


# === Return the users JSON object. ===
@app.route('/catalog/users.json')
def usersJSON():
    """
    ####Returns####
        + users:  JSON object of all users
    """
    users = session.query(User).order_by(User.name.asc())
    return jsonify(users=[u.serialize for u in users])


# === Return the catalog XML object. ===
@app.route('/catalog.xml')
def catalogXML():
    """
    ####Returns####
        + genres:  XML object of all genres and books
    """
    root = ET.Element('genres')
    return app.response_class(
        ET.tostring(
            Category.getCatalogXML(session, root),
            encoding='us-ascii',
            method='xml'),
        mimetype='application/xml')


# === Return a category XML object. ===
@app.route('/catalog/<int:category_id>/category.xml')
def categoryXML(category_id):
    """
    ####Args####
        + category_id:  the id of the category of the book

    ####Returns####
        + genre:  XML object of the genre
    """
    category = session.query(Category).filter_by(id=category_id).one()
    root = ET.Element('genre')
    return app.response_class(
        ET.tostring(
            Category.getCategoryXML(session, category.id, root),
            encoding='us-ascii',
            method='xml'),
        mimetype='application/xml')


# === Return a book XML object. ===
@app.route('/catalog/<int:category_id>/<int:item_id>/item.xml')
def itemXML(category_id, item_id):
    """
    ####Args####
        + category_id:  the id of the category of the book
        + item_id:  the id of the book

    ####Returns####
        + book:  XML object of the book
    """
    root = ET.Element('book')
    return app.response_class(
        ET.tostring(
            Item.getItemXML(session, item_id, root),
            encoding='us-ascii',
            method='xml'),
        mimetype='application/xml')


# === Return the users XML object. ===
@app.route('/users.xml')
def usersXML():
    """
    ####Returns####
        + users:  XML object of all users
    """
    root = ET.Element('users')
    return app.response_class(
        ET.tostring(
            User.getUsersXML(session, root),
            encoding='us-ascii',
            method='xml'),
        mimetype='application/xml')


# === Return the Atom feed of recently added/modified books. ===
@app.route('/recent.atom')
def recentItemsAtom():
    """
    ####Returns####
        + Recent Items:  Atom feed of recent books
    """
    return Item.getRecentItemsAtom(
        session,
        'Recent Items',
        request.url,
        request.url_root).get_response()


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
