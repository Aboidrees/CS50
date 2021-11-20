import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import requests, json

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

params = {'token': os.environ.get("API_KEY")}

@app.route("/")
# @login_required
def index():
    """Show portfolio of stocks"""
    purchases = db.execute("SELECT * FROM purchases WHERE user_id=?", 1)

    return render_template("index.html", purchases=purchases)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get('symbol')
        shares = request.form.get('shares')

        if not symbol or not shares:
            return apology("All fileds are mandetory")

        if int(shares) <= 0:
            return apology("Shares value should be posative number")

        data = lookup(symbol)

        import time

        user_id = session.get('user_id')
        name = data['name']
        price = usd(data['price'])
        symbol = data['symbol']

        _time = time.time()

        result = db.execute(
            "INSERT INTO purchases (user_id, name, symbol, price, shares, time) VALUES(?, ?, ?, ?, ?, ?)",
            user_id, name, symbol, price, shares, _time
        )

        if result:
            flash("Bought!")
            return redirect('/')
        else:
            flash("Failed!")

    return render_template("buy.html")

    # return apology("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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


@app.route("/quote", methods=["GET", "POST"])
# @login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        symbol = request.form.get("symbol")
        if symbol:
            data = lookup(symbol)
            if data is None:
                return apology("Not Found", 404)

            return render_template('quoted.html', data=data)
        else:
            return apology("Enter vaild symbol")

    return render_template('quote.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')

        if not username:
            return apology("username field can not be blank")
        else:
            result = db.execute("SELECT COUNT(*) AS username FROM users WHERE username=?", username)

            if int(result[0]['username']) >= 1:
                return apology("username already exists")

        if not password:
            return apology("password field can not be blank")

        if not cpassword:
            return apology("password confirmation field can not be blank")

        if password != cpassword:
            return apology("passwords do not match")

        password =  generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        _id = db.execute("INSERT INTO users (username, hash) VALUES (?,?)", username, password)
        if _id:
            session["user_id"]  = _id
            return redirect('/')
        else:
            return redirect('/login')

    return render_template('register.html')


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)