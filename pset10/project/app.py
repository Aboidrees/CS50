# import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, flash
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
# from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.security import generate_password_hash

from helpers import apology, login_required, status, is_selected, get_last_shift_summary
from datetime import datetime as dt

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
app.jinja_env.filters["status"] = status
app.jinja_env.filters['is_selected'] = is_selected

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///shifts.db")


@app.route('/', methods=["GET", "POST"])
@login_required
def index():
    # Add, Edit & Delete
    if request.method == 'POST':

        # Show the form used to add tasks
        if request.form.get('action') == "add":
            member_s = db.execute("SELECT * FROM members")

            return render_template('tasks/edit.html', members=member_s)

        # Shows the form for editing tasks
        if request.form.get('action') == "edit":
            task_id = request.form.get('id')

            task = db.execute("SELECT * FROM tasks where id=?", task_id)
            member_s = db.execute("SELECT * FROM members")

            if task and member_s:
                return render_template('tasks/edit.html', task=task[0], members=member_s)
            else:
                flash("Not Found")
                return redirect('/')

        # Saving the data sent from add and edit forms
        if request.form.get('action') == "save":
            task_id = request.form.get('id')
            member_id = request.form.get('member_id')
            task = request.form.get('task')
            outcome = request.form.get('outcome')

            if not task or not member_id:
                flash("Task & Member fields are required!", 'danger')

            if task_id:
                sql = 'UPDATE tasks SET member_id=?, task=?, outcome=? WHERE id=?'
                result = db.execute(sql, member_id, task, outcome, task_id)
            else:
                sql = 'INSERT INTO tasks (member_id, task, outcome) VALUES (?, ?, ?)'
                result = db.execute(sql, member_id, task, outcome)

            if result:
                flash("Saved successful1!", "success")
            else:
                flash("Failed!", 'danger')

            return redirect('/')

        # Deleting the task
        if request.form.get('action') == "delete":

            task_id = request.form.get('id')

            if task_id:
                result = db.execute("DELETE FROM tasks WHERE id=?", task_id)
                if result:
                    flash("Task has been deleted!", "success")
                else:
                    flash("Something went wrong!", "error")

                return redirect('/')
            else:
                return apology('Unauthorized access', 403)

        # Change the task status
        if request.form.get('action') == "status":

            task_id = request.form.get('id')
            time = dt.now().strftime("%Y-%m-%d %H:%M:%S")

            if task_id:
                task = db.execute("SELECT status FROM tasks WHERE id=?", task_id)[0]
                if task:
                    result = db.execute(
                        "UPDATE tasks SET status=?, finished=? WHERE id=?",
                        ("Done" if task['status'] == "Pending" else "Pending"),
                        (time if task['status'] == "Pending" else ""),
                        task_id
                    )
                    return redirect('/') if result else apology('Something went wrong!')
                else:
                    apology('Something went wrong!')
    else:
        # Default request -> shows all the tasks
        # get summary added by the last shift
        summary = get_last_shift_summary(db)

        # this condition used to render a specific task details on click
        where = " WHERE tasks.id=?" if request.args.get('id') else ''

        sql = "SELECT tasks.*, members.name FROM tasks " \
              "LEFT JOIN members ON members.id = tasks.member_id" + where

        # this condition used to render a specific task details on click
        if request.args.get('id'):
            result = db.execute(sql, int(request.args.get('id')))
        else:
            result = db.execute(sql)

        return render_template('tasks/view.html', tasks=result, summary=summary)


@app.route('/incidents', methods=["GET", "POST"])
@login_required
def incidents():
    if request.method == 'POST':

        # Show the form used to add incident
        if request.form.get('action') == "add":
            #
            return render_template('incidents/edit.html')

        # Shows the form for editing incident
        if request.form.get('action') == "edit":
            incident_id = request.form.get('id')

            result = db.execute("SELECT * FROM incidents where id=?", incident_id)

            if result:
                return render_template('incidents/edit.html', incident=result[0])
            else:
                flash("Not Found")
                return redirect('/')

        # Saving the data sent from add and edit forms
        if request.form.get('action') == "save":
            incident_id = request.form.get('id')
            member_id = session.get('member_id')
            title = request.form.get('title')
            description = request.form.get('description')

            if not title or not description:
                flash("All fields are required!", 'danger')

            if incident_id:
                sql = 'UPDATE incidents SET member_id=?, title=?, description=? WHERE id=?'
                result = db.execute(sql, member_id, title, description, incident_id)
            else:
                sql = 'INSERT INTO incidents (member_id, title, description) VALUES (?, ?, ?)'
                result = db.execute(sql, member_id, title, description)

            if result:
                flash("Saved successful1!", "success")
            else:
                flash("Failed!", 'danger')

            return redirect('/incidents')

        # Deleting the incidents
        if request.form.get('action') == "delete":

            incident_id = request.form.get('id')

            if incident_id:
                result = db.execute("DELETE FROM incidents WHERE id=?", incident_id)
                if result:
                    flash("Incident report has been deleted!", "success")
                else:
                    flash("Something went wrong!", "error")

                return redirect('/incidents')
            else:
                return apology('Unauthorized access', 403)
    else:

        # Default request -> shows all the Incidents

        # get summary added by the last shift
        summary = get_last_shift_summary(db)

        # this condition used to render a specific incident details on click
        where = " WHERE incidents.id=?" if request.args.get('id') else ''

        sql = "SELECT incidents.*, members.name FROM incidents " \
              "LEFT JOIN members ON members.id = incidents.member_id" + where

        # this condition used to render a specific incident details on click
        if request.args.get('id'):
            result = db.execute(sql, int(request.args.get('id')))
        else:
            result = db.execute(sql)

        return render_template('incidents/view.html', incidents=result, summary=summary)


@app.route('/members', methods=["GET", "POST"])
@login_required
def members():
    if request.method == 'POST':

        # Show the form used to add members
        if request.form.get('action') == 'add':
            # Show empty edit form
            return render_template('members/edit.html')

        # Shows the form for editing members
        if request.form.get('action') == 'edit':
            member_id = request.form.get('id')

            result = db.execute("select * from members where id=?", member_id)

            if result:
                return render_template('members/edit.html', member=result[0])
            else:
                flash("Not Found")
                return redirect('/members')

        # Saving the data sent from add and edit forms
        if request.form.get('action') == 'save':
            #
            member_id = request.form.get('id')

            #
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            permission = request.form.get('permission')
            role = request.form.get('role')

            if not name or not email or not phone or not permission or not role:
                flash("All member fields are required!", "danger")
                return redirect('/members')

            if member_id:
                sql = 'UPDATE members SET name=?, email=?, phone=?, permission=?, role=? WHERE id=?'
                result = db.execute(sql, name, email, phone, permission, role, member_id)

            else:
                sql = 'INSERT INTO members (name, email, phone, permission, role) VALUES (?, ?, ?, ?, ?)'
                result = db.execute(sql, name, email, phone, permission, role)

            if result:
                flash("Saved successful1!", "success")
            else:
                flash("Failed!", 'danger')

            return redirect('/members')

        # Deleting the members
        if request.form.get('action') == 'delete':
            member_id = request.form.get('id')

            if member_id:
                if int(member_id) == session.get('member_id'):
                    flash("Member can't delete his account!", "info")
                else:
                    member = db.execute("DELETE FROM members WHERE id=?", member_id)
                    if member:
                        flash("Member has been deleted!", "success")
                    else:
                        flash("Something went wrong!", "error")

                return redirect('/members')
            else:
                return apology('Unauthorized access', 403)
    else:
        # Default request -> shows all the members
        result = db.execute("SELECT * FROM members")
        return render_template('members/view.html', members=result)


@app.route('/summaries', methods=["GET", "POST"])
@login_required
def summaries():
    if request.method == 'POST':

        # Show the form used to add summaries
        if request.form.get('action') == "add":
            #
            return render_template('summaries/edit.html')

        # Shows the form for editing summaries
        if request.form.get('action') == "edit":
            summary_id = request.form.get('id')

            result = db.execute("SELECT * FROM summaries where id=?", summary_id)

            if result:
                return render_template('summaries/edit.html', summary=result[0])
            else:
                flash("Not Found")
                return redirect('/summaries')

        # Saving the data sent from add and edit forms
        if request.form.get('action') == "save":
            shift_id = session.get('shift')['id']
            summary_id = request.form.get('id')
            summary = request.form.get('summary')

            if not summary:
                flash("All fields are required!", 'danger')

            if summary_id:
                sql = 'UPDATE summaries SET shift_id=?, summary=? WHERE id=?'
                result = db.execute(sql, shift_id, summary, summary_id)
            else:
                sql = 'INSERT INTO summaries (shift_id, summary) VALUES (?, ?)'
                result = db.execute(sql, shift_id, summary)

            if result:
                flash("Saved successful1!", "success")
            else:
                flash("Failed!", 'danger')

            return redirect('/summaries')

        # Deleting the summaries
        if request.form.get('action') == "delete":

            summary_id = request.form.get('id')

            if summary_id:
                result = db.execute("DELETE FROM summaries WHERE id=?", summary_id)
                if result:
                    flash("Summary has been deleted!", "success")
                else:
                    flash("Something went wrong!", "error")

                return redirect('/summaries')
            else:
                return apology('Unauthorized access', 403)
    else:

        # this condition used to render a specific summary details on click
        where = " WHERE summaries.id=?" if request.args.get('id') else ''

        # Default request -> shows all the Summaries
        sql = "SELECT summaries.*, shifts.name, shifts.start_time, shifts.end_time " \
              "FROM summaries LEFT JOIN shifts ON shifts.id=summaries.shift_id " \
              + where + " ORDER BY created DESC"

        # this condition used to render a specific summary details on click
        if request.args.get('id'):
            result = db.execute(sql, int(request.args.get('id')))
        else:
            result = db.execute(sql)

        return render_template('summaries/view.html', summaries=result)


@app.route('/shifts', methods=["GET", "POST"])
@login_required
def shifts():
    if request.method == 'POST':

        # Show the form used to add shifts
        if request.form.get('action') == "add":
            #
            return render_template('shifts/edit.html')

        # Shows the form for editing shifts
        if request.form.get('action') == "edit":
            #
            shift_id = request.form.get('id')
            result = db.execute("SELECT * FROM shifts where id=?", shift_id)

            if result:
                return render_template('shifts/edit.html', shift=result[0])
            else:
                flash("Not Found")
                return redirect('/shifts')

        # Saving the data sent from add and edit forms
        if request.form.get('action') == "save":
            shift_id = request.form.get('id')
            name = request.form.get('name')
            start_time = request.form.get('start_time')
            end_time = request.form.get('end_time')

            if not name or not end_time or not start_time:
                flash("All fields are required!", 'danger')

            # TODO: Check if the start is before the end
            if shift_id:
                sql = 'UPDATE shifts SET name=?, start_time=?, end_time=? WHERE id=?'
                result = db.execute(sql, name, start_time, end_time, shift_id)
            else:
                sql = 'INSERT INTO shifts (name, start_time, end_time) VALUES (?, ?, ?)'
                result = db.execute(sql, name, start_time, end_time)

            if result:
                flash("Saved successful1!", "success")
            else:
                flash("Failed!", 'danger')

            return redirect('/shifts')

        # Deleting the shifts
        if request.form.get('action') == "delete":

            shift_id = request.form.get('id')

            if shift_id:
                result = db.execute("DELETE FROM shifts WHERE id=?", shift_id)
                if result:
                    flash("Shift has been deleted!", "success")
                else:
                    flash("Something went wrong!", "error")

                return redirect('/shifts')
            else:
                return apology('Unauthorized access', 403)
    else:

        # Default request -> shows all the shifts
        result = db.execute("SELECT * FROM shifts")
        return render_template('shifts/view.html', shifts=result)


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any member_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            return apology("must provide email", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM members WHERE email = ?", request.form.get("email"))
        shift = db.execute(
            "SELECT * FROM shifts "
            "WHERE start_time <= (SELECT time(?) as Time) "
            "AND end_time >= (SELECT time(?) as Time)",
            dt.now().strftime("%Y-%m-%d %H:%M:%S"), dt.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1:
            return apology("invalid username and/or password", 403)

        # Remember which user has logged-in
        session["member_id"] = rows[0]["id"]
        session['permission'] = rows[0]["permission"]
        session['role'] = rows[0]["role"]
        session['name'] = rows[0]["name"]
        session['shift'] = shift[0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        #
        return render_template("authentication/login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        name = request.form.get('name')
        role = request.form.get('role')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        if not name:
            flash('User full name field can not be blank', 'danger')
        if not role:
            flash('User role field can not be blank', 'danger')
        if not email:
            flash('User role field can not be blank', 'danger')
        if not password:
            flash('password field can not be blank', 'danger')
        if not confirmation:
            flash('password confirmation field can not be blank', 'danger')
        elif password != confirmation:
            flash('passwords do not match', 'danger')

        if not name or not role or not email or not password or password != confirmation:
            return redirect('/register')

        result = db.execute("SELECT COUNT(*) AS email FROM members WHERE email=?", email)

        if int(result[0]['email']) >= 1:
            return apology("Email already exists")
        else:
            password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

            sql = "INSERT INTO members (name, role, email, hash) VALUES (?, ?, ?, ?)"
            member_id = db.execute(sql, name, role, email, password)

            if member_id:
                flash('Registration succeeded!, try to login', 'success')
                redirect('/login')
            else:
                flash('Registration failed!, try again later.', 'danger')
                return redirect('/register')

    else:
        return render_template('authentication/register.html')


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any member_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


if __name__ == '__main__':
    app.run()


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
