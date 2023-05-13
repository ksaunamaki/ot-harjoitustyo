from services.database_service import DatabaseService


class ConfigurationRepository:
    """Maintains configuration settings in local database.
    """
    def __init__(self, database: DatabaseService):
        self._database = database
        self._default_language = "en"

    def _get_configuration_setting(self, setting_id: str) -> str:
        data = self._database.select_rows_from_table("configuration",
                                                     "key",
                                                     setting_id)

        for row in data:
            return row["value"]

        return None

    def _store_configuration_setting(self,
                                    setting_id: str,
                                    setting_data: str):
        _ = self._database.remove_row_from_table("configuration",
                                             ["key"],
                                             [setting_id])

        self._database.store_row_to_table("configuration",
                                          [setting_id, setting_data])

    def get_languge(self) -> str:
        """Get configured language.

        Returns:
            str: Language code of language configured as default.
        """
        language = self._get_configuration_setting("language")

        if language is not None:
            return language

        return self._default_language

    def store_languge(self, language_id: str):
        """Change default configured language.

        Args:
            language_id (str): Language code (en, fi) to store as default langauge.
        """
        if language_id in ["en", "fi"]:
            self._store_configuration_setting("language", language_id)

    def get_api_key(self) -> str:
        """Get configured Aviationstack API key.

        Returns:
            str: API key or None if none configured.
        """
        return self._get_configuration_setting("aviationstack_apikey")

    def store_api_key(self, api_key: str):
        """Store API key to use against Aviationstack API.

        Args:
            api_key (str): API key.
        """
        self._store_configuration_setting("aviationstack_apikey", api_key)
