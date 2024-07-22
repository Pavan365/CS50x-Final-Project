# Import standard libraries.
import functools

# Import external libraries.
from flask import Blueprint, flash, g, redirect, render_template, session, url_for
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import PasswordField, StringField
from wtforms.validators import EqualTo, InputRequired, Regexp

# Import local modules.
from .database import get_db

# Define the blueprint.
bp = Blueprint("authenticate", __name__, url_prefix="/authenticate")


class RegisterForm(FlaskForm):
    """
    Represents a register form.
    """

    username = StringField("Username", [InputRequired("Missing Username"), Regexp(r"^[\w]{4,20}$", message="Invalid Username")])
    password = PasswordField("Password", [InputRequired("Missing Password"), Regexp(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{6,20}$", message="Invalid Password")])
    confirm  = PasswordField("Confirm Password", [InputRequired("Confirm Password"), EqualTo("password", message="Passwords Do Not Match")])


class LoginForm(FlaskForm):
    """
    Represents a login form.
    """

    username = StringField("Username", [InputRequired("Missing Username"), Regexp(r"^.{4,20}$", message="Invalid Username")])
    password = PasswordField("Password", [InputRequired("Missing Password"), Regexp(r"^.{6,20}$", message="Invalid Password")])


@bp.route("/register", methods=("GET", "POST"))
def register():
    """
    Registers the user.

    Renders
    -------
    authenticate/register.html
        If the route was requested through the GET method.

    Redirects
    ---------
    authenticate.register
        If the user could not be registered. An error message is also
        flashed.

    authenticate.login
        If the user was registered. A success message is also flashed.
    """

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        hashed_password = generate_password_hash(form.password.data)

        con = get_db()
        cur = con.cursor()

        if cur.execute("SELECT * FROM users WHERE username = ? LIMIT 1", (username, )).fetchone() is not None:
            flash("Username Taken", "error")
            return redirect(url_for("authenticate.register"))

        else:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            con.commit()

            flash("Account Created!", "success")
            return redirect(url_for("authenticate.login"))

    return render_template("authenticate/register.html", form=form)


@bp.route("/login", methods=("GET", "POST"))
def login():
    """
    Logs-in the user.

    Renders
    -------
    authenticate/login.html
        If the route was requested through the GET method.

    Redirects
    ---------
    authenticate.login
        If the user could not be logged-in. An error message is also
        flashed.

    options.index
        If the user was logged-in.
    """

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        con = get_db()
        cur = con.cursor()

        user = cur.execute("""SELECT * FROM users WHERE username = ? LIMIT 1""", (username, )).fetchone()

        if user is None:
            flash("Incorrect Username Or Password", "error")
            return redirect(url_for("authenticate.login"))

        elif check_password_hash(user["password"], password):
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("options.index"))

        else:
            flash("Incorrect Username Or Password", "error")
            return redirect(url_for("authenticate.login"))

    return render_template("authenticate/login.html", form=form)


@bp.route("/logout")
def logout():
    """
    Logs-out the user.

    Redirects
    ---------
    options.index
        After the session is cleared.
    """

    session.clear()
    return redirect(url_for("options.index"))


@bp.before_app_request
def config_session():
    """ Configures the session. """

    user_id = session.get("user_id")

    if user_id is None:
        g.user = None

    else:
        g.user = user_id


def login_required(view):
    """
    Wraps a view with a function that ensures the user is logged-in.

    Parameters
    ----------
    view
        The original view.

    Returns
    -------
    wrapped_view
        The original view after being wrapped.
    """

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        """
        Ensures the user is logged-in.

        Parameters
        ----------
        **kwargs

        Returns
        -------
        view(**kwargs)
            The original view. If the user is logged in.

        Redirects
        ---------
        authenticate.login
            If the user is not logged-in.
        """

        if g.user is None:
            return redirect(url_for("authenticate.login"))

        return view(**kwargs)

    return wrapped_view

