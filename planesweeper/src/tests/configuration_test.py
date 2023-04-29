import unittest
import shutil, tempfile
import game
from services.database_service import DatabaseService
from repositories.configuration_repository import ConfigurationRepository


class TestGameConfiguration(unittest.TestCase):
    def setUp(self):
        self._test_dir = tempfile.mkdtemp()
        self._test_db_path = f"{self._test_dir}/TestConfigurations"
        self._database_service = DatabaseService(True, self._test_db_path )

    def tearDown(self):
        self._database_service.close()
        shutil.rmtree(self._test_dir)

    def test_database_resets(self):
        config_repo = ConfigurationRepository(self._database_service)
        config_repo.store_language("fi")

        self._database_service.close()

        self._database_service = DatabaseService(True, self._test_db_path)
        config_repo = ConfigurationRepository(self._database_service)

        set_lang = config_repo.get_language()

        self.assertEqual(set_lang, config_repo._default_language)

    def test_can_set_supported_languages(self):
        config_repo = ConfigurationRepository(self._database_service)

        languages = ["en", "fi"]

        for language in languages:
            config_repo.store_language(language)
            set_lang = config_repo.get_language()
            self.assertEqual(set_lang, language)
    
    def test_cannot_set_unsupported_languages(self):
        config_repo = ConfigurationRepository(self._database_service)

        language = "kr"

        config_repo.store_language(language)
        set_lang = config_repo.get_language()

        self.assertNotEqual(set_lang, language)

    def test_returns_default_language_if_not_set(self):
        config_repo = ConfigurationRepository(self._database_service)

        set_lang = config_repo.get_language()

        self.assertEqual(set_lang, config_repo._default_language)

    def test_can_set_language_via_commandline(self):
        database = DatabaseService()
        config_repo = ConfigurationRepository(database)

        set_lang = config_repo.get_language()

        language = "fi" if set_lang == "en" else "en"

        game.configure(['',f'--setlang={language}'], config_repo)

        set_lang_new = config_repo.get_language()

        self.assertEqual(set_lang_new, language)
