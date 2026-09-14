import os

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_db():
    connection = sqlite3.connect("sidequest.db")
    connection.row_factory = sqlite3.Row
    return connection

def login_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return function(*args, **kwargs)

    return decorated_function

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
@login_required
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

        if category=="carpool":
            origin=request.form.get("origin")
            destination=request.form.get("destination")
            travel_date=request.form.get("travel_date")
            travel_time=request.form.get("travel_time")
            seats=request.form.get("seats")
            estimated_fare=request.form.get("estimated_fare")

            if not origin:
                return "Please enter a valid place"

            if not destination:
                return "Please enter a valid place"

            if not travel_date:
                return "Please enter a valid date"

            if not travel_time:
                return "Please enter a valid time"

            if not seats:
                return "Please enter valid no. of seats"

            if not estimated_fare:
                return "Please enter a valid fare"

            try:
                seats = int(seats)
                estimated_fare = float(estimated_fare)
            except ValueError:
                return "Please enter valid numbers for seats and fare", 400

            if not seats>0 or  not estimated_fare>=0 :
                return "Please enter a valid number"

            user_id = session["user_id"]

            new_quest=connection.execute("INSERT INTO quests(title,description,category,user_id) VALUES(?,?,?,?) ",(title,description,category,user_id))
        
            quest_id=new_quest.lastrowid
            
            carpool_fields=connection.execute("INSERT INTO carpools(quest_id,origin,destination,travel_date,travel_time,seats,estimated_fare) VALUES(?,?,?,?,?,?,?)",(quest_id,origin,destination,travel_date,travel_time,seats,estimated_fare))
         
        connection.commit()
        connection.close()

        return redirect("/")

    else:
        return render_template("create.html")


@app.route("/quest/<int:quest_id>")
@login_required
def quest(quest_id):
    connection = get_db()

    quest = connection.execute("SELECT * FROM quests WHERE id = ?",(quest_id,)).fetchone()
    carpool = connection.execute(
        """
        SELECT *
        FROM carpools
        JOIN quests ON carpools.quest_id = quests.id
        WHERE quests.id = ?
        """,
        (quest_id,)
    ).fetchone()

    participant_count = connection.execute(
        """
        SELECT COUNT(*) AS participant_count
        FROM quest_participants
        WHERE quest_id = ?
        """,
        (quest_id,)
    ).fetchone()

    participant_count = participant_count["participant_count"]
    estimated_fare=carpool["estimated_fare"]
    fare_per_person=None
    if participant_count>0:
        fare_per_person = estimated_fare / participant_count

    total_seats = carpool["seats"] if carpool else 0
    available_seats = total_seats - participant_count

    connection.close()

    return render_template(
        "quest.html",
        quest=quest,
        carpool=carpool,
        participant_count=participant_count,
        total_seats=total_seats,
        available_seats=available_seats,
        fare_per_person=fare_per_person,
        estimated_fare=estimated_fare
    )


@app.route("/myquests")
@login_required
def myquest():
    user_id = session["user_id"]

    connection = get_db()

    quests = connection.execute(
        "SELECT * FROM quests WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,)
    ).fetchall()

    connection.close()

    return render_template("myquests.html", quests=quests)


@app.route("/quest/<int:quest_id>/join", methods=["POST"])
@login_required
def join(quest_id):

    user_id = session["user_id"]

    connection = get_db()

    # Make sure the quest exists
    quest = connection.execute(
        "SELECT * FROM quests WHERE id = ?",
        (quest_id,)
    ).fetchone()

    if quest is None:
        connection.close()
        return "Quest not found", 404

    # Only carpool quests can be joined
    if quest["category"] != "carpool":
        connection.close()
        return "This quest cannot be joined", 400

    # Get the carpool details
    carpool = connection.execute(
        "SELECT * FROM carpools WHERE quest_id = ?",
        (quest_id,)
    ).fetchone()

    if carpool is None:
        connection.close()
        return "Carpool not found", 404

    # Check whether this user already joined
    existing = connection.execute(
        """
        SELECT *
        FROM quest_participants
        WHERE quest_id = ? AND user_id = ?
        """,
        (quest_id, user_id)
    ).fetchone()

    if existing:
        connection.close()
        return "You already joined this quest", 400

    # Count current participants
    participant_count = connection.execute(
        """
        SELECT COUNT(*) AS participant_count
        FROM quest_participants
        WHERE quest_id = ?
        """,
        (quest_id,)
    ).fetchone()

    participant_count = participant_count["participant_count"]

    # Check whether the ride is full
    if participant_count >= carpool["seats"]:
        connection.close()
        return "Seats are full, please try another one", 400

    # Add the user as a participant
    connection.execute(
        """
        INSERT INTO quest_participants (quest_id, user_id)
        VALUES (?, ?)
        """,
        (quest_id, user_id)
    )

    connection.commit()
    connection.close()

    return redirect(f"/quest/{quest_id}")