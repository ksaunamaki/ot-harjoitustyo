import importlib
import inspect
from primitives.interfaces import LanguageResource


class LanguageService:

    IMPORT_LANGUAGES = ["english", "finnish"]

    def __init__(self, default_language: str = None):
        self._languages : dict[str, LanguageResource] = {}
        for language_name in LanguageService.IMPORT_LANGUAGES:
            module_name = f"services.languages.{language_name}"
            module = importlib.import_module(module_name)
            language_class = getattr(module, language_name.capitalize())
            language = language_class()

            if inspect.isclass(type(LanguageResource())):
                self._languages[language_name[0:2]] = language

        self._selected_language = None

        if default_language in self._languages:
            self._selected_language = self._languages[default_language]
        else:
            if len(self._languages) > 0:
                self._selected_language = next(iter((self._languages.items())))[1]

    def get_available_languages(self) -> list[str]:
        return list(self._languages.keys())

    def change_language(self, language_id: str):
        if language_id in self._languages:
            self._selected_language = self._languages[language_id]

    def get_text(self,
                 text_id: str,
                 format_params: list = None) -> str:
        if self._selected_language is None:
            return ""

        return self._selected_language.get_text(text_id, format_params)
