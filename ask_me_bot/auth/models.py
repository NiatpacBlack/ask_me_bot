"""This file describes the tables of users."""
from ask_me_bot.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST
from ask_me_bot.db_client.db import PostgresClient


postgres_client = PostgresClient(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
)


def create_users_table() -> None:
    """Creates a user table that stores user information from a telegram chat."""

    postgres_client.create_table(
        "users",
        """
        user_id SERIAL PRIMARY KEY, 
        user_telegram_id INTEGER NOT NULL,
        user_name VARCHAR(255) NULL,
        first_name VARCHAR(255) NULL,
        last_name VARCHAR(255) NULL,
        user_creation_date timestamp with time zone NOT NULL
        """,
    )


def create_all_auth_table() -> None:
    create_users_table()


if __name__ == '__main__':
    create_all_auth_table()
