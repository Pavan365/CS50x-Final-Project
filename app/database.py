# Import standard libraries.
import sqlite3

# Import external libraries.
from flask import current_app, g


def init_app(app):
    """ Registers database functions with the app. """

    app.teardown_appcontext(close_db)


def get_db():
    """
    Returns a connection to the database.

    Returns
    -------
    g.db : sqlite3.Connection
        A connection to the database.
    """

    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
    Closes a connection to the database.

    Parameters
    ----------
    e : error object, default = None
        Error/Exception.
    """

    db = g.pop("db", None)

    if db is not None:
        db.close()
