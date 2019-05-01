
from flask import Flask, render_template, request, redirect
from flask import session as login_session, url_for, flash, jsonify
import random
import string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
import datetime
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


# create Flask app
app = Flask(__name__)
# Google sign in ID
client_id = '198020618168-a4ieutk5gt8bhc59l2jorugjd62jijvn\
                 .apps.googleusercontent.com'

# bind to database with SQLalchemy
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine


# To check if an item is already in that category
def checkItem(item_title, category_title):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    category = session.query(Category).filter_by(title=category_title).one()
    check = session.query(Item.id).filter(
        Item.title == item_title).filter(Item.category == category)
    return session.query(check.exists()).scalar()


# Login page
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Oauth method for Google sign in
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
        oauth_flow = flow_from_clientsecrets('../client_secrets.json',
                                             scope='')
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
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != client_id:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is\
                                                    already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius:150px;\
                    -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s"
          % login_session['username'])
    print "done!"
    return output


# Revoke auth/sign out
@app.route('/gdisconnect')
def gdisconnect():
    if 'access_token' not in login_session:
        return redirect('/login')
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
    	response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s'\
        % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke\
            token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Home page showing categories and items
@app.route('/')
def showCatalog():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    catalog = session.query(Category).all()
    items = session.query(Item).order_by(Item.date_time.desc()).limit(5).all()
    return render_template('catalog.html', category=catalog, items=items)


# Show all items in category
@app.route('/category/<string:category_title>/items')
def showCategories(category_title):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    category = session.query(Category).filter_by(title=category_title).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    session.close()
    return render_template('category.html', category=category, items=items)


# Show a specific item
@app.route('/category/<string:category_title>/<string:item_title>')
def showItem(category_title, item_title):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    catalog = session.query(Category).filter_by(title=category_title).one()
    item = session.query(Item).filter_by(title=item_title).first()
    session.close()
    return render_template('item.html', category=catalog, item=item)


# JSON endpoint to get item information
@app.route('/category/<string:category_title>/<string:item_title>.json')
def itemJSON(item_title, category_title):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    category = session.query(Category).filter_by(title=category_title).one()
    item = session.query(Item).filter_by(
        title=item_title).filter_by(category_id=category.id).one()
    session.close()
    return jsonify(item=item.serialize)


# Add a new item if logged in
@app.route('/item/new', methods=['GET', 'POST'])
def newItem():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        now = datetime.datetime.now()
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        if checkItem(request.form['title'], request.form['category']):
            flash("Item already exists!")
            catalog = session.query(Category).all()
            session.close()
            return render_template('newitem.html', category=catalog)
        else:
            category = session.query(Category).filter_by(
                title=request.form['category']).one()
            newItem = Item(title=request.form['title'],
                           description=request.form['description'],
                           category=category,
                           date_time=now.strftime("%Y-%m-%d %H:%M"))
            session.add(newItem)
            session.commit()
            session.close()
            return redirect(url_for('showCatalog'))
    else:
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        catalog = session.query(Category).all()
        session.close()
        return render_template('newitem.html', category=catalog)


# Edit item if logged in
@app.route('/category/<string:category_title>/<string:item_title>/edit',
           methods=['GET', 'POST'])
def editItem(category_title, item_title):
    if 'username' not in login_session:
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    catalog = session.query(Category).all()
    category = session.query(Category).filter_by(title=category_title).one()
    editItem = session.query(Item).filter_by(
        title=item_title).filter_by(category_id=category.id).one()
    if request.method == 'POST':
        if checkItem(request.form['title'], request.form['category']):
            flash("Item already exists!")
            return render_template('edititem.html', category=catalog,
                                   category_title=category_title,
                                   item=editItem)
        else:
            if request.form['title']:
                editItem.title = request.form['title']
            if request.form['description']:
                editItem.description = request.form['description']
            if request.form['category']:
                editCategory = session.query(Category).filter_by(
                    title=request.form['category']).first()
                editItem.category_id = editCategory.id
            session.add(editItem)
            session.commit()
            session.close()
            return redirect(url_for('showItem',
                            category_title=editItem.category.title,
                            item_title=editItem.title))
    else:
        return render_template('edititem.html',
                               category=catalog,
                               category_title=category_title,
                               item=editItem)


# Delete item if logged in
@app.route('/category/<string:category_title>/<string:item_title>/delete',
           methods=['GET', 'POST'])
def deleteItem(item_title, category_title):
    if 'username' not in login_session:
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    category = session.query(Category).filter_by(title=category_title).one()
    itemToDelete = session.query(Item).filter_by(
        title=item_title).filter_by(category_id=category.id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        session.close()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deleteitem.html',
                               item=itemToDelete,
                               category=itemToDelete.category)


if __name__ == "__main__":
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000)
