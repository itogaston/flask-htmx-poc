from app.models.PostModel import Post
from app.repositories.PostRepository import PostRepository
from app.db import new_cursor
import logging


class PostRepositoryImp(PostRepository):
    def new(self, new_row: Post) -> int:
        cur = new_cursor()
        cur.execute(
            """"INSERT INTO post (title, body, author_id)" " VALUES (?, ?, ?)", """,
            (new_row.title, new_row.body, new_row.author_id),
        )

        new_id = cur.fetchone()
        if new_id and len(new_id):
            new_id = new_id[0]
        else:
            new_id = 0

        return new_id

    def get_by_id(self, id_val: int) -> Post:
        cur = new_cursor(Post)
        post = cur.execute(
            "SELECT p.id, title, body, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        ).fetchone()
        return post

    def get_all(self) -> list[Post]:
        logging.info("get all posts")

        cur = new_cursor(Post)
        cur.execute(
            "SELECT p.id, title, body, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " ORDER BY created DESC"
        )
        posts = cur.fetchall()

        return posts


def new_post_repo() -> PostRepository:
    return PostRepositoryImp()
