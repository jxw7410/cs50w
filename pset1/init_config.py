import asyncio
from flask import Flask, redirect, flash, render_template, request, session, jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)

#Turning off logging
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

#Prevents flask from sending cached scripts to the browser (why does it do this?)
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure app session
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/users.db' #default database
app.config["SQLALCHEMY_BINDS"] = {'books' : 'sqlite:///database/books.db'}#additional databases, these need bind keys
app.secret_key = "463e07020e43de2e932516aa6e853350" #use if not using Session(app)
#Session(app) #use if not using secret_key


#init database
db = SQLAlchemy(app)