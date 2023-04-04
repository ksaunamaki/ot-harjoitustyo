from enum import Enum


class GameState(Enum):
    INITIAL = 0
    INITIALIZE_NEW_GAME = 1
    SINGLE_GAME = 2
    CHALLENGE_GAME = 3
    GAME_OVER = 4
    EXIT = 99
