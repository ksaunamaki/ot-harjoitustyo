import unittest
from services.language_service import LanguageService


class TestLanguageService(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_languages_available(self):
        service = LanguageService()
        languages = service.get_available_languages()

        self.assertNotEqual(len(languages), 0)

    def test_default_language_works(self):
        service = LanguageService("en")
        
        str_data = service.get_text("test")
        self.assertEqual(str_data, "en_test")

    def test_languages_switch_works(self):
        service = LanguageService()
        languages = service.get_available_languages()

        for language in languages:
            service.change_language(language)
            str_data = service.get_text("test")

            self.assertEqual(str_data, f"{language}_test")
    
