from primitives.game_mode import GameMode

class GameInitialization:
    def __init__(self, level: int, mode: GameMode = GameMode.SINGLE_GAME):
        self.level = level
        self.mode = mode
