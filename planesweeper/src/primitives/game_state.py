from enum import Enum

class GameState(Enum):
    Initial = 0
    InitializeNewGame = 1
    SingleGame = 2
    ChallengeGame = 3
    GameOver = 4
    Exit = 99