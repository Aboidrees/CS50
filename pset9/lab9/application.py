import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form.get('add'):
            print('Added')
            name = request.form.get('name')
            month = request.form.get('month')
            day = request.form.get('day')

            if name or month or day:
                db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", name, month, day)

        if request.form.get('delete'):
            print('deleted')
            _id = request.form.get('id')
            db.execute("DELETE FROM birthdays WHERE id = ?", _id)

        return redirect("/")

    else:

        birthdays = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", birthdays=birthdays)


