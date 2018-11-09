import os
from flask import Flask, redirect, flash, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from flask_socketio import SocketIO, emit

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
app.config["SECRET_KEY"] = 'secret_key_gen_12345676!!!3345' #use if not using Session(app)
#Session(app) #use if not using secret_key

socketio = SocketIO(app)

#hardcoded remote localhost link to run code.
print("Link: https://ide50-jan-wu.cs50.io:8080/")

