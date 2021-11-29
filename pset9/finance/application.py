import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd
from datetime import datetime as dt

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# export API_KEY=
# export FLASK_APP=application.py


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


@app.route("/")
@login_required
def index():
    # Save the session in variable
    user_id = session.get('user_id')

    operations_records = db.execute(
        "SELECT id, name, symbol, SUM(price) AS price, SUM(shares) AS shares "
        "FROM operations "
        "WHERE user_id=? GROUP BY symbol", user_id
    )

    user = db.execute("SELECT * FROM users WHERE id=?", user_id)

    operations = []
    for operation in operations_records:
        data = lookup(operation['symbol'])

        operation['price'] = data['price']
        operations.append(operation)

    return render_template("index.html", operations=operations, cash=user[0]['cash'])


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        # Save the form variable
        symbol = request.form.get('symbol')
        shares = request.form.get('shares')

        # Save the session in variable
        user_id = session.get('user_id')

        if not symbol or not shares:
            return apology("All fields are mandatory")

        if not shares.isdigit() or int(shares) <= 0:
            return apology("Shares value should be positive number and greater than zero")

        data = lookup(symbol)
        if data is None:
            return apology("Not Found")

        user = db.execute("SELECT * FROM users WHERE id=?", user_id)
        available_cash = float(user[0]['cash'])

        if available_cash >= int(shares) * data['price']:
            time = dt.now().strftime("%Y-%m-%d %H:%M:%S")
            record_operation = db.execute(
                "INSERT INTO operations (user_id, name, symbol, price, shares, type, time) "
                "VALUES(?, ?, ?, ?, ?, 'buy', ?)",
                user_id, data['name'], data['symbol'], data['price'], shares, time
            )
            if record_operation:
                new_cash = available_cash - int(shares) * data['price']
                update_cash = db.execute("UPDATE users SET cash=? WHERE id=?", new_cash, user_id)
                if update_cash:
                    flash("Sold!")
                    return redirect('/')
                else:
                    apology("Couldn't update user cash")
            else:
                apology("Couldn't register the operation")
        else:
            apology('user cannot afford the number of shares at the current price')
    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    result = db.execute("SELECT * FROM operations WHERE user_id=?", 1)
    operations = []

    for operation in result:
        if operation['type'] == "sel":
            operation['shares'] *= -1
        operations.append(operation)

    return render_template("history.html", operations=operations)


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
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        symbol = request.form.get("symbol")
        if symbol:
            data = lookup(symbol)
            if data is None:
                return apology("Not Found")

            return render_template('quoted.html', data=data)
        else:
            return apology("Enter valid symbol")

    return render_template('quote.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        if not username:
            return apology("username field can not be blank")
        else:
            result = db.execute("SELECT COUNT(*) AS username FROM users WHERE username=?", username)

            if int(result[0]['username']) >= 1:
                return apology("username already exists")

        if not password:
            return apology("password field can not be blank")

        if not confirmation:
            return apology("password confirmation field can not be blank")

        if password != confirmation:
            return apology("passwords do not match")

        password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        _id = db.execute("INSERT INTO users (username, hash) VALUES (?,?)", username, password)
        if _id:
            session["user_id"] = _id
            return redirect('/')
        else:
            return redirect('/login')

    return render_template('register.html')


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        # Save the form variable
        symbol = request.form.get('symbol')
        shares = request.form.get('shares')

        # Save the session in variable
        user_id = session.get('user_id')

        # check if variable is empty
        if not symbol or not shares:
            return apology("All fields are mandatory")

        # check if the shares is numaric
        if not shares.isdigit() or int(shares) <= 0:
            return apology("Shares value should be positive number and greater than zero")

        # get stock data
        data = lookup(symbol)

        # check if the stock data is empty
        if data is None:
            return apology("Not Found")

        # get user information to update the cash
        user = db.execute("SELECT * FROM users WHERE id=?", user_id)
        available_cash = float(user[0]['cash'])

        # get company held shares information for check and update
        user_shares = db.execute(
            "SELECT id, name, symbol, SUM(price) AS price, SUM(shares) AS shares "
            "FROM operations "
            "WHERE user_id=? and symbol=? GROUP BY symbol ", user_id, symbol
        )
        available_shares = user_shares[0]['shares']

        # check if the available stock shares can satisfy the sell operation
        if available_shares >= int(shares):
            time = dt.now().strftime("%Y-%m-%d %H:%M:%S")
            record_operation = db.execute(
                "INSERT INTO operations (user_id, name, symbol, price, shares, type, time) "
                "VALUES(?, ?, ?, ?, ?, 'sell', ?)",
                user_id, data['name'], data['symbol'], data['price'], (int(shares) * -1), time
            )
            # check if the operation is registered
            if record_operation:
                new_cash = available_cash + int(shares) * data['price']
                update_cash = db.execute("UPDATE users SET cash=? WHERE id=?", new_cash, user_id)

                # check if the cash is updated
                if update_cash:

                    # save flash success and redirect
                    flash("Sold!")
                    return redirect('/')
                else:

                    # apology if cash updated fails
                    return apology("Couldn't update user cash")
            else:

                # apology if the operation is not registered
                return apology("Couldn't register the operation")

        else:

            # apology if no sufficient stock shares
            return apology('user cannot afford the number of shares at the current price')

    # list of available stock shares
    held_stocks = db.execute("SELECT * FROM operations GROUP BY symbol HAVING shares>0")
    return render_template("sell.html", held_stocks=held_stocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
