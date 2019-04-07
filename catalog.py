from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
import datetime

#create Flask app
app = Flask(__name__)

#bind to database with SQLalchemy
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

@app.route('/')
def showCatalog():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    catalog = session.query(Category).all()
    session.close()
    return render_template('catalog.html', category = catalog)

@app.route('/category/<string:category_title>/items')
def showCategories(category_title):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    catalog = session.query(Category).filter_by(title=category_title).one()
    #items = session.query(Item).filter_by(category=category_title).all()
    session.close()
    return render_template('category.html', category = catalog)

@app.route('/category/<string:category_title>/<string:item_title>')
def showItem(category_title, item_title):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    catalog = session.query(Category).filter_by(title=category_title).one()
    item = session.query(Item).filter_by(title=item_title).one()
    session.close()
    return render_template('item.html', category = catalog, item = item)

@app.route('/item/new')
#To-DO - add category name and item in route
def createItem():
    return "This page will allow a logged in user to create a specific item"

@app.route('/item/edit')
#To-DO - add category name and item in route
def editItem():
    return "This page will allow a logged in user to edit a specific item"

@app.route('/item/delete')
#To-DO - add category name and item in route
def deleteItem():
    return "This page will allow a logged in user to delete a specific item"

@app.route('/item/JSON')
#To-DO - add category name and item in route
def jsonItem():
    return "This page will allow an api json endpoint"

if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)