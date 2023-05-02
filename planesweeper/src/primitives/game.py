from enum import Enum


class GameState(Enum):
    """Main loop state for current game program execution.
    """
    INITIAL = 0
    INITIALIZE_NEW_GAME = 1
    RUN_GAME = 2
    GAME_OVER = 3
    GET_INITIALS = 4
    PROCESS_CHALLENGE_ROUND_RESULT = 5
    EXIT = 99

class GameMode(Enum):
    """Game mode selected.
    """
    SINGLE_GAME = 0
    CHALLENGE_GAME = 1

class ChallengeGameProgress:
    """Progress tracking for on-going challenge game.
    """
    def __init__(self):
        self.current_level = 1
        self.score = 0
        self.level_failures = 0
        self.last_won = False
        self.message_shown_start = 0

class GameInitialization:
    """Initialization data used for a new game session.
    """
    def __init__(self,
                 level: int,
                 mode: GameMode = GameMode.SINGLE_GAME,
                 ongoing_progress: ChallengeGameProgress = None):
        self.level = level
        self.mode = mode
        self.ongoing_progress = ongoing_progress
