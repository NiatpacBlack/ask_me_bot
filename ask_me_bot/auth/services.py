"""This file contains the business logic of the authentication's module."""
from datetime import datetime

import pytz

from ask_me_bot.auth.models import postgres_client
from ask_me_bot.config import TIME_ZONE


def create_new_user_if_not_exist(user_info: dict) -> None:
    """Creates a new user with data about his telegram account, if the user is not yet in the database."""
    user_telegram_id = user_info['id']
    user_name = user_info.get('username', None)
    first_name = user_info.get('first_name', None)
    last_name = user_info.get('last_name', None)

    query = f"""
        INSERT INTO users (user_telegram_id, user_name, first_name, last_name, user_creation_date)
        SELECT '{user_telegram_id}', '{user_name}', '{first_name}', '{last_name}', '{datetime.now(pytz.timezone(TIME_ZONE))}'
        WHERE NOT EXISTS (
            SELECT * FROM users
            WHERE user_telegram_id='{user_telegram_id}'
        );
    """
    postgres_client.cursor.execute(query)
    postgres_client.db_connect.commit()
