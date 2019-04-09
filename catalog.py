from flask import Flask, render_template, request, redirect, url_for
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
    category = session.query(Category).filter_by(title=category_title).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    session.close()
    return render_template('category.html', category = category, items = items)

@app.route('/category/<string:category_title>/<string:item_title>')
def showItem(category_title, item_title):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    catalog = session.query(Category).filter_by(title=category_title).one()
    item = session.query(Item).filter_by(title=item_title).one()
    session.close()
    return render_template('item.html', category = catalog, item = item)

@app.route('/item/new', methods=['GET', 'POST'])
def newItem():
    if request.method == 'POST':
        now = datetime.datetime.now()
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        category = session.query(Category).filter_by(title=request.form['category']).first()
        newItem = Item(title=request.form['title'], description=request.form['description'], category=category, date_time=now.strftime("%Y-%m-%d %H:%M") )
        session.add(newItem)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        catalog = session.query(Category).all()
        return render_template('newitem.html', category= catalog)

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