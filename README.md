# Catalog Web App

Solution for Assignment 2 of the [Udacity](https://www.udacity.com/) Full Stack nanodegree. The task is to create an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system

## Install

Download [Python 2.7](https://www.python.org/downloads/) - required to run the python flask web application. Documentation available [here](https://docs.python.org/)

### Dependencies

Install [Flask](http://flask.pocoo.org/docs/1.0/installation/) and [SQLAlchemy](https://docs.sqlalchemy.org/en/13/intro.html)

```command
pip install Flask
pip install SQLAlchemy
```

### Create Database and Populate

The creation of the database and categories are only required for the initial install. To create the Sqlite database run:

```command
python database_setup.py
```

Database contains two tables, Category with id and title columns and Items with id, title, description, category_id, cateogroty and date_time. To populate categories run:

```command
python create_categories.py
```

If you would like to add your own categories, edit the list in the file create_categories.py

### Run Flask Web App

To run the web app:

```command
python catalog.py
```

Open a browser and go to http://localhost:5000 to view the application.