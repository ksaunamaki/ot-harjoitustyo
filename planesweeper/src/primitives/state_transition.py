from primitives.game import GameState


class StateTransition:
    def __init__(self, next_state: GameState, data=None):
        self.next = next_state
        self.data = data
