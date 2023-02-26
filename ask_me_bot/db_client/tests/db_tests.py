from unittest import TestCase, main

from psycopg2 import errors

from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST
from ask_me_bot.db_client.db import PostgresClient
from ask_me_bot.db_client.exceptions import CantTableError


class PostgresClientTest(TestCase):
    """Tests for methods of the PostgresClient class."""

    def setUp(self):
        self.postgres_client = PostgresClient(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
        )

        self.postgres_client.create_table(
            "test_table",
            """
            Id SERIAL PRIMARY KEY,
            FirstName CHARACTER VARYING(30),
            LastName CHARACTER VARYING(30),
            Email CHARACTER VARYING(30),
            Age INTEGER
            """,
        )

    def test_type_select_all_tables_from_db(self):
        """Test of the return data type of the select_all_tables_from_db function."""

        self.assertEqual(
            type(self.postgres_client.select_all_tables_name_from_db()), list
        )

    def test_type_select_all_from_table(self):
        """Test of the return data type of the select_all_from_table function."""

        # Testing the data type if available.
        self.assertEqual(
            type(self.postgres_client.select_all_from_table(table_name="test_table")),
            list,
        )

    def test_error_select_all_from_table(self):
        """Test of the select_all_from_table function with invalid arguments."""

        # If an invalid table name or data type is passed to the function, a custom error should appear.
        with self.assertRaises(CantTableError) as e:
            self.postgres_client.select_all_from_table("1234556732523626")
            self.assertEqual(
                "You have entered a table name that does not exist.",
                e.exception.args[0],
            )

        with self.assertRaises(CantTableError) as e:
            self.postgres_client.select_all_from_table(252)
            self.assertEqual(
                "You have entered a table name that does not exist.",
                e.exception.args[0],
            )

    def test_type_select_columns_from_table(self):
        """Test of the return data type of the select_columns_from_table function."""

        # Testing the data type if available.
        self.assertEqual(
            type(
                self.postgres_client.select_columns_from_table(
                    "test_table", "id", "firstname"
                )
            ),
            list,
        )

    def test_error1_select_columns_from_table(self):
        """Test 1 of the select_columns_from_table function with invalid arguments."""

        # If an invalid table name is passed to the function, a special psycopg2 module error should occur.
        with self.assertRaises(errors.UndefinedTable) as e:
            self.postgres_client.select_columns_from_table("123214", "id", "age")
            self.assertEqual(
                'отношение "123214" не существует',
                e.exception.args[0],
            )

    def test_error2_select_columns_from_table(self):
        """Test 2 of the select_columns_from_table function with invalid arguments."""

        # If an invalid column name is passed to the function, a special psycopg2 module error should be raised.
        with self.assertRaises(errors.UndefinedColumn) as e:
            self.postgres_client.select_columns_from_table("test_table", "id23", "age")
            self.assertEqual(
                'столбец "id23" не существует',
                e.exception.args[0],
            )

    def test_error3_select_columns_from_table(self):
        """Test 3 of the select_columns_from_table function with invalid arguments."""

        # If an invalid column or table data type is passed to the function, a TypeError should be raised.
        with self.assertRaises(TypeError) as e:
            self.postgres_client.select_columns_from_table("test_table", 1234, "age")
            self.postgres_client.select_columns_from_table(1234, "id", "age")
            self.assertEqual(
                "SQL identifier parts must be strings",
                e.exception.args[0],
            )

    def test_create_and_delete_table(self):
        """Test of the function that creates a table in the database and test of the function that deletes the table."""

        # Get the number of all tables before adding.
        tables_count = len(self.postgres_client.select_all_tables_name_from_db())

        # Create a test table.
        self.postgres_client.create_table(
            table_name="new_test_table",
            values_pattern="test TEXT, test1 VARCHAR(20), test2 INTEGER",
        )

        # Checking that there are 1 more tables after adding.
        self.assertEqual(
            len(self.postgres_client.select_all_tables_name_from_db()), tables_count + 1
        )

        # Delete the added test table.
        self.postgres_client.delete_table("new_test_table")

        # Checking that the number of tables has decreased.
        self.assertEqual(
            len(self.postgres_client.select_all_tables_name_from_db()), tables_count
        )

    def test_insert_and_delete_value_in_table(self):
        """Test of a function that adds data to a specific table and a function that deletes data from a table."""

        # Checking the number of elements in the table before adding.
        values_count = len(self.postgres_client.select_all_from_table("test_table"))

        # Adding test data to the table.
        self.postgres_client.insert_in_table(
            table_name="test_table",
            firstname="testtest",
            lastname="testtest",
            email="testtest@testmail.ru",
            age="1224",
        )

        # Compare the number of elements in the table after adding.
        self.assertEqual(
            len(self.postgres_client.select_all_from_table("test_table")),
            values_count + 1,
        )

        # Delete a test row from a table.
        self.postgres_client.delete_value_in_table(
            "test_table", "email='testtest@testmail.ru'"
        )

        # Compare that the number of elements in the table is equal to the original.
        self.assertEqual(
            len(self.postgres_client.select_all_from_table("test_table")), values_count
        )

    def test_update_table_where(self):
        """A test of a function that updates data in a specific table with a condition."""

        # Create a test table.
        self.postgres_client.create_table(
            table_name="new_test_table",
            values_pattern="firstname VARCHAR(50), lastname VARCHAR(50), email VARCHAR(50), age INTEGER",
        )

        # Adding test data to the table.
        self.postgres_client.insert_in_table(
            table_name="new_test_table",
            firstname="testtest",
            lastname="testtest",
            email="testtest@testmail.ru",
            age="1224",
        )

        # Adding more test data to the table.
        self.postgres_client.insert_in_table(
            table_name="new_test_table",
            firstname="testtest",
            lastname="testtest",
            email="testtest@testmail.ru",
            age="888",
        )

        # Update column data in a table.
        self.postgres_client.update_table_where(
            "new_test_table", "age", "10", "age=888"
        )

        # Finding updated data in a table.
        self.assertEqual(
            self.postgres_client.select_columns_from_table("new_test_table", "age"),
            [(1224,), (10,)],
        )

        # Delete the added test table.
        self.postgres_client.delete_table("new_test_table")


if __name__ == "__main__":
    main()
