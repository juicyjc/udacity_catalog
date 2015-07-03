# udacity_catalog
Project Three: Item Catalog

This is the repository for Project Three of the Udacity Fullstack Web Developer Nanodegree - Item Catalog.

## Quick start

To run this application:

1. Clone this repository - https://github.com/juicyjc/udacity_catalog.git
2. Make sure that you have the version of Python and the modules listed below.
3. From the command line, run the command "python database_setup.py" to set up the database.
4. From the command line, run the command "python load_data.py" to add sample data to the database.
5. From the command line, run the command "python application.py" to start the web server.
6. Navigate to http://localhost:8000/ in a web browser.
7. Take a look in the docs folder to see the code Pycco-formatted.
8. Enjoy!

## Python and Module Versions
+ Python 2.7.6
+ Flask - 0.10.1
+ Flask-SeaSurf - 0.2.0
+ SQLAlchemy - 0.8.4

## API Endpoints - JSON, XML, and Atom
#### Users
+ JSON - http://localhost:8000/catalog/users.json
+ XML - http://localhost:8000/users.xml

#### Catalog
+ JSON - http://localhost:8000/catalog.json
+ XML - http://localhost:8000/catalog.xml

#### Genre
+ JSON - http://localhost:8000/catalog/category_id/category.json
+ XML - http://localhost:8000/catalog/category_id/category.xml

#### Book
+ JSON - http://localhost:8000/catalog/category_id/item_id/item.json
+ XML - http://localhost:8000/catalog/category_id/item_id/item.xml

#### Atom - Recent Items Feed
+ http://localhost:8000/recent.atom


