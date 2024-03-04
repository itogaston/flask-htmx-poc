import sqlite3
import click
from flask import current_app, g
import logging

logging.info("dbing")


def get_db():
    logging.info("getting db")
    if "db" not in g:
        logging.info("db not in g, creating...")
        g.db = sqlite3.connect(
            "instance/flaskr.sqlite", detect_types=sqlite3.PARSE_DECLTYPES
        )
    return g.db


def new_cursor(row_factory=None):
    logging.info("new cursor")
    db = get_db()

    if row_factory is None:
        db.row_factory = sqlite3.Row
    else:
        db.row_factory = row_factory
    return db.cursor()


def close_db(e=None):
    logging.info("closing db conn")
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    logging.info("init db")
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
