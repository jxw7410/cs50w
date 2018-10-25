from init_config import *

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def dictFormat(self):
        return {"username" : self.username}

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
userdbEngine = create_engine('sqlite:///database/bookreview.db')
mSession = sessionmaker(bind=userdbEngine)
sessionengine = mSession()

#create a metadata table ORM
def create_table(table_name, engine = userdbEngine):
    metadata = MetaData(engine)
    Table(table_name, metadata, Column('Id', Integer, primary_key=True),
                                Column('User_Id', Integer, unique=True),
                                Column('Rating', Float, nullable=False),
                                Column('Value', String(250), nullable=False))
    if not engine.dialect.has_table(engine, table_name):
        metadata.create_all()

#return table
def fetch_table(table_name, engine = userdbEngine):
    metadata = MetaData(engine)
    Table(table_name, metadata, Column('Id', Integer, primary_key=True),
                                Column('User_Id', Integer, unique=True),
                                Column('Rating', Float, nullable=False),
                                Column('Value', String(250), nullable=False))
    if not engine.dialect.has_table(engine, table_name):
        return None
    return metadata.tables[table_name]

#To post message into table
def insert_table(table, string, rating, userid):
    connection = userdbEngine.connect()
    connection.execute(table.insert(values={"User_Id" : userid, "Rating" : rating, "Value" : string}))
    connection.close()
    print(sessionengine.query(table).all())