from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

#create Flask app
app = Flask(__name__)

#bind to database with SQLalchemy
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

@app.route('/')
def showCatalog():
    return render_template('catalog.html')

@app.route('/category')
#To-DO - add category name in route
def showCategories():
    return "This page will show a specific category"

@app.route('/item')
#To-DO - add category name and item in route
def showItem():
    return "This page will show a specific item"

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