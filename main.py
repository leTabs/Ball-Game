# importing dependencies
from flask import Flask, render_template, redirect, url_for, request, session, jsonify
import os, re
from flask_socketio import join_room, leave_room, send, SocketIO

from database import log, register
from chat_themes import themes
from account_standard import valid_username, valid_key, confirm_key

# flask standard
app = Flask(__name__, static_folder="static")
app.secret_key = os.urandom(6)

# sockets inclusion
socketio = SocketIO(app)


# opening panel
@app.route("/")
def index():
    return render_template("index.html")

# ---------------------------------------------------------------------

# logging in presidure
@app.route("/", methods=["POST"])
def log_in():
        return redirect(url_for("find_chat"))

# ---------------------------------------------------------------------

# signing up presidure
@app.route("/", methods=["POST"])
def sign_up():
        return redirect(url_for("find_chat")) 
# ------------------------------------------------------------------------

# finding chat endpoint
@app.route("/find_chat", methods=["GET"])
def find_chat():
    return render_template("pop.html")

# Flask conclusion
if __name__ == "__main__":
    host = '127.0.0.1'
    port = 5000
    socketio.run(app, host=host, port=port, debug=True, allow_unsafe_werkzeug=True)
