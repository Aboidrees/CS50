from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("member_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def status(value):
    """Format value as USD."""
    return '<span class="p-2 bg-' + value + ' rounded-circle status"></span>'


def is_selected(array, key, value):
    if array:
        return 'selected' if array[key] == value else ''


def get_last_shift_summary(db):
    result = db.execute("SELECT * FROM summaries ORDER BY created DESC LIMIT 1 ")
    return result[0] if result else ''
