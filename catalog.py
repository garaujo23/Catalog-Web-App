from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
import datetime

#create Flask app
app = Flask(__name__)

#bind to database with SQLalchemy
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

#To check if an item is already that category in the database
def checkItem(item_title, category_title):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    category = session.query(Category).filter_by(title=category_title).one()
    check = session.query(Item.id).filter(Item.title==item_title).filter(Item.category == category)
    return session.query(check.exists()).scalar()


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
    item = session.query(Item).filter_by(title=item_title).first()
    session.close()
    return render_template('item.html', category = catalog, item = item)

@app.route('/category/<string:category_title>/<string:item_title>.json')
def itemJSON(item_title, category_title):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    category = session.query(Category).filter_by(title=category_title).one()
    item = session.query(Item).filter_by(title=item_title).filter_by(category_id=category.id).one()
    return jsonify(item=item.serialize)

@app.route('/item/new', methods=['GET', 'POST'])
def newItem():
    if request.method == 'POST':
        now = datetime.datetime.now()
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        if checkItem(request.form['title'],request.form['category']):
            flash("Item already exists!")
            catalog = session.query(Category).all()
            return render_template('newitem.html', category= catalog)
        else:
            category = session.query(Category).filter_by(title=request.form['category']).one()
            newItem = Item(title=request.form['title'], description=request.form['description'], category=category, date_time=now.strftime("%Y-%m-%d %H:%M") )
            session.add(newItem)
            session.commit()
            return redirect(url_for('showCatalog'))
    else:
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        catalog = session.query(Category).all()
        return render_template('newitem.html', category= catalog)

@app.route('/category/<string:category_title>/<string:item_title>/edit', methods=['GET', 'POST'])
def editItem(category_title, item_title):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    catalog = session.query(Category).all()
    category = session.query(Category).filter_by(title=category_title).one()
    editItem = session.query(Item).filter_by(title=item_title).filter_by(category_id=category.id).one()
    if request.method == 'POST':
        if checkItem(request.form['title'], request.form['category']):
            flash("Item already exists!")
            return render_template('edititem.html', category = catalog, category_title=category_title, item=editItem)
        else:
            if request.form['title']:
                editItem.title = request.form['title']
            if request.form['description']:
                editItem.description = request.form['description']
            if request.form['category']:
                editCategory = session.query(Category).filter_by(title=request.form['category']).first()
                editItem.category_id = editCategory.id
            session.add(editItem)
            session.commit()
            return redirect(url_for('showItem', category_title = editItem.category.title, item_title = editItem.title))
    else:
        return render_template('edititem.html', category = catalog, category_title=category_title, item=editItem)

@app.route('/category/<string:category_title>/<string:item_title>/delete', methods=['GET', 'POST'])
def deleteItem(item_title,category_title):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    category = session.query(Category).filter_by(title=category_title).one()
    itemToDelete = session.query(Item).filter_by(title=item_title).filter_by(category_id=category.id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deleteitem.html', item=itemToDelete, category=itemToDelete.category)

if __name__ == "__main__":
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host = '0.0.0.0', port = 5000)