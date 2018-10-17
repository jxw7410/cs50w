import os
from helpers import *
from dbModels import *
from flask import flash, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

'''
Original source code had SQLAlchemy engine, but if flask quick start (in dbModels) is available, don't need engine
check out the page SQLAchemy flask, it basically does some auto configurations for users with regards to SQLAlchemy.session
'''
#create tables that aren't already in db
db.create_all();


@app.route("/login", methods = ["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        _username = request.form.get("username")
        _password = request.form.get("password")
        dbUser = User.query.filter_by(username=_username).first()
        if dbUser is None:
            return jsonify({"request": False})
        if not check_password_hash(dbUser.password, _password):
            return jsonify({"request": False})
        session["user_id"] = dbUser.id
        return jsonify({"request" : True})
    return render_template("login.html")


@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        _username = request.form.get("username")
        _password = request.form.get("password")
        _passwordAgain = request.form.get("passwordAgain")

        if _password != _passwordAgain:
            return jsonify({"request" : False})
        
    return render_template("register.html")

@app.route("/")
@login_required
def index():
    return render_template("index.html")


