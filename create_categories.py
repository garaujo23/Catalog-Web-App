import sqlite3
import datetime

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except AssertionError as e:
        print(e)
 
    return None

def main():
    database = "catalog.db"
    categories = [(1, 'Cricket'), (2, 'Hockey'), (3, 'Tennis'), (4, 'Soccer'), (5, 'Rugby'), (6, 'Basketball'), (7, 'Frisbee'), (8, 'Snowboarding'), (9, 'Rock Climbing'), (10, 'Foosball'), (11, 'Skating')]
    #now = datetime.datetime.now()
    #item = [(1, 'bat', 'This is a test cricket bat description', 'Cricket', now.strftime("%Y-%m-%d %H:%M"))]

    conn = create_connection(database)
    if conn is not None:
        cursor = conn.cursor()
        cursor.executemany("insert into category values (?,?);", categories)
        #cursor.executemany("insert into item values (?,?,?,?,?);", item)
        conn.commit()
        conn.close
    else:
        print("Error cannot connect to database, check file is in same directory")

if __name__ == '__main__':
    main()