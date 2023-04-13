from pygame_renderer import PygameRenderer
from pygame_ui_events import PygameEvents
from primitives.game_state import GameState
from primitives.game_initialization import GameInitialization
from loop import CoreLoop
from services.database_service import DatabaseService


def main():
    renderer = PygameRenderer()
    pygame_events = PygameEvents()
    game_database = DatabaseService()
    core_loop = CoreLoop(renderer, pygame_events, game_database)

    state = GameState.INITIALIZE_NEW_GAME
    game_initialization = GameInitialization(1)

    core_loop.run(state, game_initialization)

if __name__ == "__main__":
    main()
