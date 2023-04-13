class SingleGameHighscore:

    def __init__(self, level: int, time: float, initials: str):
        self.level = level
        self.time = time
        self.initials = initials

class ChallengeGameHighscore:

    def __init__(self, score: int, initials: str):
        self.score = score
        self.initials = initials
