from pygame_renderer import PygameRenderer
from pygame_ui_events import PygameEvents
from loop import CoreLoop
from services.database_service import DatabaseService


def main():
    renderer = PygameRenderer()
    pygame_events = PygameEvents()
    game_database = DatabaseService()
    core_loop = CoreLoop(renderer, pygame_events, game_database)

    core_loop.run()

if __name__ == "__main__":
    main()
