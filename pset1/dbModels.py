from init_config import *

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    def dictFormat(self):
        return {"username" : self.username}

    def GetUserName(self):
        return self.username

    def Add(self):
        db.session.add(self)
        db.session.commit()

class Books(db.Model):
    __bind_key__="books"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable = False)

    def dictFormat(self):
        return {"isbn" : self.isbn, "title" : self.title, "author" : self.author, "year" : self.year}

#create all tables
db.create_all();

#open up engine for dynamic ORM, stores info as metadata.
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
userdbEngine = create_engine('sqlite:///database/bookreviews.db')
mSession = sessionmaker(bind=userdbEngine)
sessionengine = mSession()

#create a metadata table ORM
def create_table(table_name, engine = userdbEngine):
    metadata = MetaData(engine)
    Table(table_name, metadata, Column('Id', Integer, primary_key=True),
                                Column('User', String(32), nullable=False, unique=True),
                                Column('Rating', Float, nullable=False),
                                Column('Value', String(4000), nullable=False))
    if not engine.dialect.has_table(engine, table_name):
        metadata.create_all()

#return table
def fetch_table(table_name, engine = userdbEngine):
    metadata = MetaData(engine)
    Table(table_name, metadata, Column('Id', Integer, primary_key=True),
                                Column('User', String(32), nullable=False, unique=True),
                                Column('Rating', Float, nullable=False),
                                Column('Value', String(4000), nullable=False))
    if not engine.dialect.has_table(engine, table_name):
        return None
    return metadata.tables[table_name]


def get_table_data(table, user):
    try:
        query = sessionengine.query(table).filter_by(User = user).first()
    except:
        return {"rating" : 0.0, "Review" : "Error, Please Reload"}

    return {"rating" : query[2], "review" : query[3]}


def get_table_data_other_users(table, user):
    try:
        query = sessionengine.query(table).filter(table.c.User != user).limit(5).all()
    except:
        return None
    ret = []
    for item in query:
        ret.append({"user": item[1], "rating" : item[2], "review" : item[3]})
    return ret

#command functions
#To post message into table
def insert_table(table, string, rating, user):
    connection = userdbEngine.connect()
    transaction = connection.begin()
    try:
        connection.execute(table.insert(values={"User" : user, "Rating" : rating, "Value" : string}))
        transaction.commit()
    except:
        transaction.rollback()
        connection.close()
        return False
    connection.close()
    return True

def delete_table(table, user):
    connection = userdbEngine.connect()
    transaction = connection.begin()
    try:
        connection.execute(table.delete().where(table.c.User == user))
        transaction.commit()
    except:
        transaction.rollback()
        connection.close()
        return False
    connection.close()
    return True

def update_table(table, review, rating, user):
    connection = userdbEngine.connect()
    transaction = connection.begin()
    try:
        connection.execute(table.update(values = {"Rating" : rating, "Value" : review}).where(table.c.User == user))
        transaction.commit()
    except:
        transaction.rollback()
        connection.close()
        return False
    connection.close()
    return True





