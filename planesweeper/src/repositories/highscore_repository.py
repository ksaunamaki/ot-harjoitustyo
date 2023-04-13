from primitives.highscores import SingleGameHighscore,ChallengeGameHighscore
from services.database_service import DatabaseService


class HighScoreRepository:

    def __init__(self, database: DatabaseService):
        self._database = database

    def get_single_highscores(self, level: int) -> list[SingleGameHighscore]:
        data = self._database.get_rows_from_table("single_highscores")
        highscores: list[SingleGameHighscore] = []

        for row in data:
            if int(row["level"]) != level:
                continue

            highscore = SingleGameHighscore(row["level"],
                                            row["time"],
                                            row["initials"])
            highscores.append(highscore)

        return sorted(highscores, key= lambda highscore: highscore.time)

    def get_challenge_highscores(self) -> list[ChallengeGameHighscore]:
        data = self._database.get_rows_from_table("challenge_highscores")
        highscores: list[ChallengeGameHighscore] = []

        for row in data:
            highscore = ChallengeGameHighscore(row["score"],
                                            row["initials"])
            highscores.append(highscore)

        return sorted(highscores, key= lambda highscore: highscore.score, reverse= True)

    def is_single_score_eligible(self, level: int, time: float):
        # store high-score only if within 5 best
        current_highscores = self.get_single_highscores(level)

        if len(current_highscores) < 5:
            return True

        max_time = max(map(lambda x: x.time, current_highscores))
        if max_time > time:
            return True

        return False

    def store_single_highscore(self, level: int, time: float, initials: str):
        if not self.is_single_score_eligible(level, time):
            return

        current_highscores = self.get_single_highscores(level)

        if len(current_highscores) >= 5:
            max_time = max(map(lambda x: x.time, current_highscores))
            if not self._database.remove_row_from_table("single_highscores",
                                                      ("level", "time"),
                                                      (level, max_time)):
                return

        self._database.store_row_to_table("single_highscores", (level, time, initials))
