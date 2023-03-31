from pygame_renderer import PygameRenderer
from pygame_ui_events import PygameEvents
from primitives.game_state import GameState
from primitives.game_initialization import GameInitialization
from loop import CoreLoop

def main():
    renderer = PygameRenderer()
    pygame_events = PygameEvents()
    coreLoop = CoreLoop(renderer, pygame_events)

    state = GameState.InitializeNewGame
    gameInitialization = GameInitialization(1, True)

    coreLoop.run(state, gameInitialization)

if __name__ == "__main__":
    main()