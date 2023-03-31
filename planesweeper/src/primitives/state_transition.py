from primitives.game_state import GameState

class StateTransition:
    def __init__(self, nextState: GameState, data = None):
        self.next = nextState
        self.data = data