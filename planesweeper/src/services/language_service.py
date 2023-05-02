import importlib
import inspect
from primitives.interfaces import LanguageResource


class LanguageService:
    """Facilitates getting language-specific text strings for the UI.
    """

    IMPORT_LANGUAGES = ["english", "finnish"]

    def __init__(self, default_language: str = None):
        """Initialize language services.

        Args:
            default_language (str, optional): Language to use as default.
                Defaults to None which uses first language in loaded list of languages.
        """
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
        """Gets all available languages loaded by the language service.

        Returns:
            list[str]: Language codes available.
        """
        return list(self._languages.keys())

    def change_language(self, language_id: str):
        """Changes default language used for returning texts.

        Args:
            language_id (str): Language code (en, fi, ...) to use.
        """
        if language_id in self._languages:
            self._selected_language = self._languages[language_id]

    def get_text(self,
                 text_id: str,
                 format_params: list = None) -> str:
        """Gets language-specific version of text string.

        Args:
            text_id (str): Text identifier of the text to retrieve.
            format_params (list, optional): Formatting parameters to apply against
                retrieved text if it contains format specifiers ({0} etc.).
                Defaults to None.

        Returns:
            str: Specified text or text identifier if it could not be found.
        """
        if self._selected_language is None:
            return text_id

        return self._selected_language.get_text(text_id, format_params)
