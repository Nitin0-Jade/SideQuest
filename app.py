import os

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_db():
    connection = sqlite3.connect("sidequest.db")
    connection.row_factory = sqlite3.Row
    return connection

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return "must provide username", 400
        elif not password:
            return "must provide password", 400
        elif not confirmation:
            return "must provide confirmation", 400
        elif password != confirmation:
            return "passwords must match", 400

        connection = get_db()

        existing = connection.execute("SELECT * FROM users WHERE username = ?",(username,)).fetchall()
        if existing:
            return "username already exists", 400

        hashed = generate_password_hash(password)
        connection.execute("INSERT INTO users (username, hash) VALUES (?, ?)",(username, hashed))
        connection.commit()
        new_user = connection.execute("SELECT id FROM users WHERE username = ?",(username,)).fetchone()
        session["user_id"] = new_user[0]["id"]
        connection.close()

        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Ensure username was submitted
        if not request.form.get("username"):
            return "must provide username", 403

        # Ensure password was submitted
        elif not request.form.get("password"):
            return "must provide password", 403

        # Query database for username
        connection=get_db()

        user = connection.execute(
            "SELECT * FROM users WHERE username = ?",(username,)
        ).fetchone()

        # Ensure username exists and password is correct
        if user is None or not check_password_hash(user["hash"],password):
            return "invalid username and/or password", 403

        # Remember which user has logged in
        session["user_id"] = user["id"]

        connection.close()

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/")
def index():
    """Show the SideQuest homepage."""

    connection = get_db()

    quests = connection.execute(
        """
        SELECT *
        FROM quests
        ORDER BY created_at DESC
        """
    ).fetchall()

    connection.close()

    return render_template("index.html", quests=quests)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title=request.form.get("title")
        description=request.form.get("description")
        category=request.form.get("category")
        connection=get_db()

        if not title:
            return "Please give valid Title"
        if len(title)<0 or len(title)>10:
            return "Please use a Valid title of 10 words"
        
        if not description:
            return "Please give a Valid description"
        if len(description)<0 or len(description)>100:
            return "Please write within limit(100 words)"
        
        if not category:
            return "Please return a valid category"
         
        #to add category options

        user_id = session["user_id"]

        connection.execute("INSERT INTO quests(title,description,category,user_id) VALUES(?,?,?,?) ",title,description,category,user_id)
        connection.commit()
        connection.close()
        return redirect("/")

    else:
        return render_template("create.html")


@app.route("/quest/<int:quest_id>")
def quest(quest_id):
    connection=get_db()
    quest=connection.execute("SELECT *FROM quests WHERE id = ?",(quest_id,)).fetchone()
    connection.close()
    return render_template("quest.html", quest=quest)
    

@app.route("/myquests")
def myquest():
    user_id=session["user_id"]
    connection=get_db()
    quests=connection.execute("SELECT *FROM quests WHERE user_id = ? ORDER BY created_at DESC",(user_id,)).fetchall()
    connection.close()
    return render_template("myquests.html",quests=quests)




