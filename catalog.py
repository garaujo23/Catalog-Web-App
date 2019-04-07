from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def showCatalog():
    return "This page will show all categories and latest items"

@app.route('/catalog')
#To-DO - add category name in route
def showCategories():
    return "This page will show a specific categories"

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

if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)