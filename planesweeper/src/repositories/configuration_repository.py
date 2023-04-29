from services.database_service import DatabaseService


class ConfigurationRepository:

    def __init__(self, database: DatabaseService):
        self._database = database
        self._default_language = "en"

    def get_language(self) -> str:
        data = self._database.select_rows_from_table("configuration",
                                                     "key",
                                                     "language")

        for row in data:
            return row["value"]

        return self._default_language

    def store_language(self, language: str):
        if language not in ["en", "fi"]:
            return

        _ = self._database.remove_row_from_table("configuration",
                                             ["key"],
                                             ["language"])

        self._database.store_row_to_table("configuration",
                                          ("language", language))
