from flask import Flask
from flask import Flask, render_template
from flask import Flask, flash, redirect, render_template, request, session
from helpers import login_required
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3 as sql

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.secret_key = b'P\x9b\xf2\xc7\x14\xc8mb1!\x96\xd9\xeb\x06\xbf>'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
@login_required
def index():
    return render_template('index.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    
    db_con = sql.connect("password.db")
    db = db_con.cursor()
    """Register user"""
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        
        rows = db.execute("SELECT * FROM users WHERE username = ?", (username,))
        rows = db.fetchall()

        # # Ensure username exists and password is correct
        if len(rows) == 1:
            return render_template("register.html", message="Username already taken")
            

        p = generate_password_hash(password)
        print(p)

        # db.execute("INSERT INTO users (username, hash) VALUES(%s,'" + p + "')s" %username)
        db.execute("INSERT INTO users (username, hash) VALUES(?,?)", (username, p))
        db_con.commit()

        # Redirect user to home page
        return redirect("login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    db_con = sql.connect("password.db")
    db = db_con.cursor()

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", (username,))
        rows = db.fetchall()

        if(len(rows) != 1):
            return render_template("login.html", message="Both Username and password is required")

        if rows[0][1] != username:
            # return render_template("login.html", message="Invalid username")
            return flash("pop ubibb")

        if not check_password_hash(rows[0][2], password):
            return render_template("login.html", message="Invalid password")

         # Remember which user has logged in
        session["user_id"] = rows[0][0]

         # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
         return render_template("login.html")



