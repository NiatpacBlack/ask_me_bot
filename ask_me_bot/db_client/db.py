import psycopg2
from psycopg2 import sql, errors

from ask_me_bot.db_client.exceptions import CantTableError


class PostgresClient:
    """Class for working with PostgresQL database."""

    def __init__(self, dbname, user, password, host):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.db_connect = psycopg2.connect(
            dbname=self.dbname, user=self.user, password=self.password, host=self.host
        )
        self.cursor = self.db_connect.cursor()

    def __del__(self):
        self.cursor.close()
        self.db_connect.close()

    def select_all_tables_name_from_db(self) -> list[tuple[str, ...]] | list[None]:
        """Returns a list of tuples containing the names of all tables in the database."""
        self.cursor.execute(
            """
            SELECT table_name FROM information_schema.tables \
            WHERE table_schema NOT IN ('information_schema','pg_catalog');
            """
        )

        return self.cursor.fetchall()

    def select_columns_from_table(
        self, table_name: str, *args: str
    ) -> list[tuple[str, ...]]:
        """Returns data from columns passed to args from table table_name."""
        query = sql.SQL("SELECT {} FROM {}").format(
            sql.SQL(",").join(map(sql.Identifier, args)), sql.Identifier(table_name)
        )
        self.cursor.execute(query)

        return self.cursor.fetchall()

    def select_all_from_table(self, table_name: str) -> list[tuple[str, ...]]:
        """Returns all data from table table_name."""
        try:
            self.cursor.execute("SELECT * FROM {}".format(table_name))
        except errors.SyntaxError:
            raise CantTableError("You have entered a table name that does not exist")

        return self.cursor.fetchall()

    def create_table(self, table_name: str, values_pattern: str) -> None:
        """
        Creates a new table table_name with the given fields and field parameters from values_pattern.

        Fields and values_pattern parameters are passed by pattern: "test TEXT, test1 VARCHAR(20), test2 INTEGER".
        """
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS {}({})".format(table_name, values_pattern)
        )
        self.db_connect.commit()

    def insert_in_table(self, table_name: str, **kwargs: str) -> None:
        """
        Appends the data passed in kwargs to the table table_name.

        It is important that the data must be strings, otherwise the function will not work!
        """
        insert = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table_name),
            sql.SQL(", ").join(map(sql.Identifier, kwargs.keys())),
            sql.SQL(", ").join(map(sql.Literal, kwargs.values())),
        )
        self.cursor.execute(insert)
        self.db_connect.commit()

    def delete_table(self, table_name: str) -> None:
        """Removes the table table_name from the database."""
        query = """DROP TABLE IF EXISTS {} CASCADE;""".format(table_name)
        self.cursor.execute(query)
        self.db_connect.commit()

    def update_table_where(
        self,
        table_name: str,
        set_column: str,
        set_column_value: str,
        where_pattern: str,
    ) -> None:
        """
        Updates the column passed to set_column with the data passed to set_column_value,
        given the condition passed to where_pattern.

        where_pattern must match the sql syntax after WHERE.
        for example:
        "firstname = 'Sasha'" or "id = 25 AND firstname = 'Tomas'" etc.
        """

        update = sql.SQL("UPDATE {} SET {}={} WHERE {}").format(
            sql.Identifier(table_name),
            sql.Identifier(set_column),
            sql.Literal(set_column_value),
            sql.SQL(where_pattern),
        )
        self.cursor.execute(update)
        self.db_connect.commit()

    def delete_value_in_table(self, table_name: str, where_pattern: str) -> None:
        """
        Removes a record from the table table_name that matches the entered where_pattern.

        where_pattern must match the sql syntax after WHERE.
        for example:
        "firstname = 'Sasha'" or "id = 25 AND firstname = 'Tomas'" etc.
        """

        query = """DELETE FROM {} WHERE {};""".format(table_name, where_pattern)
        self.cursor.execute(query)
        self.db_connect.commit()
