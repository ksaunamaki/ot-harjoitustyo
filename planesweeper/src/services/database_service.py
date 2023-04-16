import os
import sqlite3


class DatabaseService:

    def _drop_existing_tables(self):
        try:
            self._connection.execute("drop table if exists single_highscores;")
            self._connection.execute("drop table if exists challenge_highscores;")
        except sqlite3.OperationalError:
            self._is_available = False

    def _initialize_tables(self):
        try:
            self._connection.execute("create table single_highscores(level, time, initials);")
            self._connection.execute("create table challenge_highscores(score, initials);")
        except sqlite3.OperationalError:
            self._is_available = False

    def _initialize_database(self, database_path: str, create_as_new: bool):
        try:
            self._connection = sqlite3.connect(database_path)
        except sqlite3.OperationalError:
            self._is_available = False

        if create_as_new and self._is_available:
            # initialize as new database either for real or by request
            self._drop_existing_tables()
            self._initialize_tables()

        self._connection.row_factory = sqlite3.Row

    def __init__(self, create_as_new = False, database_path = None):
        if database_path is None:
            name = ".planesweeper.db"
            directory = os.path.dirname(__file__)
            database_path = os.path.join(directory, "..", name)
            if not os.path.exists(database_path):
                create_as_new = True

        self._connection = None
        self._is_available = True
        self._initialize_database(database_path, create_as_new)

        self._value_placeholders = {}

    def get_rows_from_table(self, table: str) -> list[sqlite3.Row]:
        data: list[sqlite3.Row] = []

        if not self._is_available:
            return data

        try:
            results = self._connection.execute(f"select * from {table}")
        except sqlite3.OperationalError:
            return data

        row = results.fetchone()
        while row is not None:
            data.append(row)
            row = results.fetchone()

        return data

    def _get_value_placeholders(self, data: list) -> str:
        elements = len(data)
        if elements in self._value_placeholders:
            placeholders = self._value_placeholders[elements]
            return placeholders

        placeholders = ""

        for _ in range(elements):
            placeholders += "?, "

        self._value_placeholders[elements] = placeholders[0:-2]

        return self._value_placeholders[elements]

    def _get_key_value_placeholders(self, keys: list) -> str:
        placeholders = ""

        for key in keys:
            placeholders += f"{key} = ? and "

        return placeholders[0:-5]

    def store_row_to_table(self, table: str, data: list) -> bool:
        if not self._is_available:
            return False

        try:
            self._connection.execute(
                f"insert into {table} values ({self._get_value_placeholders(data)})",
                data)
            self._connection.commit()
        except sqlite3.OperationalError:
            return False

        return True

    def remove_row_from_table(self, table: str, keys: list, values: list) -> bool:
        if not self._is_available:
            return False

        try:
            self._connection.execute(
                f"delete from {table} where {self._get_key_value_placeholders(keys)}",
                values)
            self._connection.commit()
        except sqlite3.OperationalError:
            return False

        return True
