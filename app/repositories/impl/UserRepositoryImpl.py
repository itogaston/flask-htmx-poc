from app.db import new_cursor
from app.models.UserModel import User
from app.repositories.UserRepository import UserRepository
import logging


class UserPostgreSQL(UserRepository):
    def new(self, new_row: User) -> int:
        cur = new_cursor()
        cur.execute(
            """INSERT INTO user
            (username, passwd)
            VALUES
            (?, ?)
            ON CONFLICT (username)
            DO NOTHING
            RETURNING id;
        """,
            (new_row.username, new_row.passwd),
        )

        new_id = cur.fetchone()
        logging.debug(f"new user id: {new_id}")
        if new_id and len(new_id):
            new_id = new_id[0]
        else:
            new_id = 0

        return new_id

    def get_by_id(self, id_val: int) -> User:
        cur = new_cursor(User)
        cur.execute(
            """
        SELECT id, username, passwd
        FROM user
        WHERE id = ?
        """,
            (id_val,),
        )

        return cur.fetchone()

    def get_by_username(self, username_val: str) -> User:
        logging.info(f"select by username {username_val}")
        cur = new_cursor(User)
        user = cur.execute(
            "SELECT * FROM user WHERE username = ?",
            (username_val,),
        ).fetchone()
        logging.info(user)
        return user


def new_user_repo() -> UserRepository:
    return UserPostgreSQL()
