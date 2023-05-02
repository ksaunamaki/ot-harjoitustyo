from primitives.game import GameState


class StateTransition:
    """Transition from one game main loop state to another with context specific data.
    """
    def __init__(self, next_state: GameState, data=None):
        """Initialize state transition.

        Args:
            next_state (GameState): Next game loop state to switch to.
            data (_type_, optional): Next state's parameter data. Defaults to None.
        """
        self.next = next_state
        self.data = data
