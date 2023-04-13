from enum import Enum


class GameState(Enum):
    INITIAL = 0
    INITIALIZE_NEW_GAME = 1
    RUN_GAME = 2
    GAME_OVER = 3
    GET_INITIALS = 4
    EXIT = 99
