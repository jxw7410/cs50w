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
