from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from app.models.PostModel import Post

from app.views.AuthView import login_required
from app.repositories.impl.PostRepositoryImpl import new_post_repo

bp = Blueprint("blog", __name__)
post_repository = new_post_repo()


@bp.route("/")
def index():
    posts = post_repository.get_all()
    return render_template("blog/index.html", posts=posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            post = Post()
            post.title = title
            post.body = body
            post.author_id = g.user["id"]

            post_repository.new(post)
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


def get_post(id, check_author=True):
    post = post_repository.get_by_id(id)

    if post is None or post == []:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post.author_id != g.user["id"]:
        abort(403)

    return post


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    post = get_post(id)
    return redirect(url_for("blog.index"))
