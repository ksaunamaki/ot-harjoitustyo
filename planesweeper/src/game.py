import sys
from pygame_renderer import PygameRenderer
from pygame_events import PygameEvents
from loop import CoreLoop
from services.database_service import DatabaseService
from services.language_service import LanguageService
from repositories.configuration_repository import ConfigurationRepository


def run_game(game_database: DatabaseService,
             config_repo: ConfigurationRepository):
    """Initialize and run main game loop.
    """
    language_service = LanguageService(config_repo.get_language())

    renderer = PygameRenderer(language_service.get_text("window_title"))
    pygame_events = PygameEvents()

    core_loop = CoreLoop(renderer,
                         pygame_events,
                         game_database,
                         language_service)
    core_loop.run()

    game_database.close()

def print_options():
    print()
    print("options:")
    print("  -setlang=[en|fi]  set game language (en by default)")
    print()

def set_language(args,
                 config_repo: ConfigurationRepository):
    parts = args.split("=")

    if parts[1].lower() in ["en", "fi"]:
        config_repo.store_language(parts[1].lower())
        return

    print_options()

def configure(args,
              config_repo: ConfigurationRepository):
    """Handle game configuration from command-line parameters.
    """
    if args[1] == "--?":
        print_options()
    elif args[1].startswith("--setlang="):
        set_language(args[1], config_repo)
    else:
        print_options()

def reset_database(game_database: DatabaseService):
    """Reset game's local database to initial state.
    """
    game_database.close()
    game_database = DatabaseService(True)

if __name__ == "__main__":
    database = DatabaseService()
    repository = ConfigurationRepository(database)

    if len(sys.argv) > 1:
        if sys.argv[1] == "reset":
            reset_database(database)
        else:
            configure(sys.argv, repository)
    else:
        run_game(database, repository)

    database.close()
