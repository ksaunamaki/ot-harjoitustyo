import os
import sqlite3


class DatabaseService:
    """Handles low-level SQLite3 database routines for accessing game database.
    """

    def _drop_existing_tables(self):
        try:
            self._connection.execute("DROP TABLE IF EXISTS single_highscores;")
            self._connection.execute("DROP TABLE IF EXISTS challenge_highscores;")
            self._connection.execute("DROP TABLE IF EXISTS configuration;")
            self._connection.execute("DROP TABLE IF EXISTS api_state;")
        except sqlite3.OperationalError:
            self._is_available = False

    def _initialize_tables(self):
        try:
            self._connection.execute(
                "CREATE TABLE IF NOT EXISTS single_highscores(level, time, initials);")
            self._connection.execute(
                "CREATE TABLE IF NOT EXISTS challenge_highscores(score, initials);")
            self._connection.execute(
                "CREATE TABLE IF NOT EXISTS configuration(key, value);")
            self._connection.execute(
                "CREATE TABLE IF NOT EXISTS api_state(key, value);")
        except sqlite3.OperationalError:
            self._is_available = False

    def _initialize_database(self, database_path: str, create_as_new: bool):
        try:
            # we MUST disable check for access from multiple threads as game's background
            # operations may utilize the connection too
            self._connection = sqlite3.connect(database_path, check_same_thread=False)
        except sqlite3.OperationalError:
            self._is_available = False

        if create_as_new and self._is_available:
            # initialize as new database either for real or by request
            self._drop_existing_tables()

        self._initialize_tables()

        self._connection.row_factory = sqlite3.Row

    def __init__(self, create_as_new = False, database_path = None):
        """Initialize database connection.

        Args:
            create_as_new (bool, optional): Create all tables anew regardless of if
                they alredy exist in the database. Defaults to False.
            database_path (_type_, optional): Fully-qualified path to the database file
                to use. Defaults to None in which case database is created inside the same
                directory as the game's root.
        """
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

    def close(self):
        """Flushes all pending data and closes the database file. To avoid any lost data
            this method should always called at the end of program when there has been
            any modifications against the database.
        """
        if self._connection is not None:
            self._connection.close()

    def get_rows_from_table(self, table: str) -> list[sqlite3.Row]:
        """Retrieve all currently existing rows in the specified table.

        Args:
            table (str): Table to get all rows from.

        Returns:
            list[sqlite3.Row]: Row data.
        """
        data: list[sqlite3.Row] = []

        if not self._is_available:
            return data

        try:
            results = self._connection.execute(f"SELECT * FROM {table}")
        except sqlite3.OperationalError:
            return data

        row = results.fetchone()
        while row is not None:
            data.append(row)
            row = results.fetchone()

        return data

    def select_rows_from_table(self,
                               table: str,
                               column, value) -> list[sqlite3.Row]:
        """Retrieve row(s) from specified table filtering based on single column value.

        Args:
            table (str): Table to get row(s) from.
            column (_type_): Column to use to filter returned row(s) on.
            value (_type_): Column value to use to filter returned row(s) on.

        Returns:
            list[sqlite3.Row]: Matching rows.
        """
        data: list[sqlite3.Row] = []

        if not self._is_available:
            return data

        try:
            results = self._connection.execute(
                f"SELECT * FROM {table} WHERE {column} = ?",
                [value])
        except sqlite3.OperationalError:
            return data

        row = results.fetchone()
        while row is not None:
            data.append(row)
            row = results.fetchone()

        return data

    def select_row_from_table(self,
                              table: str,
                              column, value) -> sqlite3.Row:
        """Retrieve single/first row from specified table filtering based on single column value.

        Args:
            table (str): Table to get row from.
            column (_type_): Column to use to filter returned row on.
            value (_type_): Column value to use to filter returned row on.

        Returns:
            sqlite3.Row: First row or None if nothing matches.
        """
        rows = self.select_rows_from_table(table, column, value)

        if rows is None or len(rows) == 0:
            return None

        return rows[0]

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
        """Store new row into specified table using supplied column values.

        Args:
            table (str): Table to store new row to.
            data (list): Column values for new row, must match order of columns in table
                specification!

        Returns:
            bool: True if row could be added, False otherwise.
        """
        if not self._is_available:
            return False

        try:
            self._connection.execute(
                f"INSERT INTO {table} VALUES ({self._get_value_placeholders(data)})",
                data)
            self._connection.commit()
        except sqlite3.OperationalError:
            return False

        return True

    def remove_row_from_table(self, table: str, keys: list, values: list) -> bool:
        """Remove existing row from specified table using supplied matching values.

        Args:
            table (str): Table to remove row from.
            keys (list): Columns to match removed row on.
            values (list): Column values to match removed row on.

        Returns:
            bool: True if operation was successful (regardless if such row 
                actually existed or not), False otherwise.
        """
        if not self._is_available:
            return False

        try:
            self._connection.execute(
                f"DELETE FROM {table} WHERE {self._get_key_value_placeholders(keys)}",
                values)
            self._connection.commit()
        except sqlite3.OperationalError:
            return False

        return True
