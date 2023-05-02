class SingleGameHighscore:
    """High-score board entry (time) for a won single game, specific for a level.
    """
    def __init__(self, level: int, time: float, initials: str):
        self.level = level
        self.time = time
        self.initials = initials

class ChallengeGameHighscore:
    """High-score board entry (score) for a won challenge game.
    """
    def __init__(self, score: int, initials: str):
        self.score = score
        self.initials = initials
