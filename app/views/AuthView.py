import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.models.UserModel import User
from app.repositories.impl.UserRepositoryImpl import new_user_repo

import logging

bp = Blueprint("auth", __name__, url_prefix="/auth")
user_repo = new_user_repo()


@bp.route("/register", methods=("GET", "POST"))
def register():
    logging.info("registering")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        user = User()
        user.username = username
        user.passwd = password
        logging.info(f"new user: {user}")

        if error is None:
            try:
                user_repo.new(user)
            except Exception as e:
                logging.error(f"Error creating user\n{e}")
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None
        logging.info(f"form login: {username} {password}")
        user = user_repo.get_by_username(username)
        logging.info(f"user check: {user}")
        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user.passwd, password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = user_repo.get_by_id(user_id)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
