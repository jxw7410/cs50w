import os
from flask import Flask, redirect, flash, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from threading import Lock

app = Flask(__name__)
app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#Turning off logging
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Configure app session
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "It's a secret for a reason."

socketio = SocketIO(app, async_mode=None)
thread = None
thread_lock = Lock()

#hardcoded remote localhost link to run code.
print("Link: https://ide50-jan-wu.cs50.io:8080/")

