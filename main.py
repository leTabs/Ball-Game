# importing dependencies
from flask import Flask, render_template, redirect, url_for, request, session, jsonify
import sqlite3, os , hashlib, re
from flask_socketio import join_room, leave_room, send, SocketIO

#from database import log, register
#from chat_themes import themes
#from account_standard import valid_username, valid_key, confirm_key

# flask standard
app = Flask(__name__, static_folder="static")
app.secret_key = os.urandom(6)

# sockets inclusion
socketio = SocketIO(app)
 
# database
connection = sqlite3.connect('gameDatabase.db')
cursor = connection.cursor()
cursor.execute("""    
    CREATE TABLE IF NOT EXISTS user_account_data (
       username TEXT UNIQUE NOT NULL,
       password TEXT NOT NULL,
       score INT DEFAULT NULL,
       games ITN DEFAULT NULL,
       easy INT DEFAULT NULL,
       normal INT DEFAULT NULL,
       hard INT DEFAULT NULL,
       impossible INT DEFAULT NULL
    )
""")
connection.commit()
connection.close()

# opening panel
@app.route("/")
def index():
    session.clear()
    return render_template("index.html")
# ---------------------------------------------------------------------
# logging in presidure
@app.route("/", methods=["POST"])
def log_in():
    session.clear()
    session["logged"] = False
    username = request.form["username"]
    password = request.form["password"]
    connection = sqlite3.connect('gameDatabase.db')
    cursor = connection.cursor()
    cursor.execute("SELECT password FROM user_account_data WHERE username = ?", (username,))
    result = cursor.fetchone()
    print("[LOOK RESULT:]", result)
    if result is None:
        return render_template("index.html", error="Invalid data")
    else:
        hashed_password = result[0]
        hashed_input_password = hashlib.sha256(password.encode()).hexdigest()
        if hashed_input_password != hashed_password:
            return render_template("index.html", error="Invalid data02")
        else:
            session["logged"] = True
            return redirect(url_for("general_panel"))
        
    
    return

@app.route("/sign_up_form", methods=["GET"])
def sign_up_form():
    return render_template("signUp.html")
    
@app.route("/signing_up", methods=["POST"])
def signing_up():
    username = request.form["username"]
    password = request.form["password"]
    session["logged"] = False 
    
    connection = sqlite3.connect('gameDatabase.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_account_data WHERE username = ?", (username,))
    if cursor.fetchone() is not None:
        return render_template("signUp.html", error="Unvailable Username")
    else:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        print("[LOOK HASHED]", hashed_password)
        cursor.execute("INSERT INTO user_account_data (username, password) VALUES (?, ?)", (username, hashed_password))
        connection.commit()
        connection.close()
        session["logged"] = True
        return redirect(url_for("general_panel"))

@app.route("/general_panel", methods=["GET"])
def general_panel():
    if "logged" not in session:
        return render_template("index.html")
    else:
        return render_template("game_general_panel.html")
# Flask conclusion
if __name__ == "__main__":
    host = '127.0.0.1'
    port = 5000
    socketio.run(app, host=host, port=port, debug=True, allow_unsafe_werkzeug=True)
