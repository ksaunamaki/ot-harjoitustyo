from primitives.highscores import SingleGameHighscore,ChallengeGameHighscore
from services.database_service import DatabaseService


class HighScoreRepository:
    """Maintains game's high-scores in local database.
    """
    def __init__(self, database: DatabaseService):
        self._database = database

    def get_single_highscores(self, level: int) -> list[SingleGameHighscore]:
        """Gets single game high-scores for level.

        Args:
            level (int): Level to get high-scores for.

        Returns:
            list[SingleGameHighscore]: List of high-score results.
        """
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
        """Gets challenge game high-scores.

        Returns:
            list[ChallengeGameHighscore]: List of high-score results.
        """
        data = self._database.get_rows_from_table("challenge_highscores")
        highscores: list[ChallengeGameHighscore] = []

        for row in data:
            highscore = ChallengeGameHighscore(row["score"],
                                            row["initials"])
            highscores.append(highscore)

        return sorted(highscores, key= lambda highscore: highscore.score, reverse= True)

    def is_single_score_eligible(self, level: int, time: float) -> bool:
        """Check if completion time for a level in single game 
            is eligible for inclusion in high-score list.
            Only 5 fastest times will be stored / level.

        Args:
            level (int): Level to check high-scores for.
            time (float): Time to check for a level's high-scores.

        Returns:
            bool: True if time can be included in high-score list.
        """
        current_highscores = self.get_single_highscores(level)

        if len(current_highscores) < 5:
            return True

        max_time = max(map(lambda x: x.time, current_highscores))
        if max_time > time:
            return True

        return False

    def store_single_highscore(self, level: int, time: float, initials: str):
        """Store single game completion time for a level with player initials as high-score.

        Args:
            level (int): Level for which to store high-score result.
            time (float): Completion time to store as a high-score result.
            initials (str): Player's initials to store for time.
        """
        if not self.is_single_score_eligible(level, time):
            return

        current_highscores = self.get_single_highscores(level)

        if len(current_highscores) >= 5:
            max_time = max(map(lambda x: x.time, current_highscores))
            if not self._database.remove_row_from_table("single_highscores",
                                                      ["level", "time"],
                                                      [level, max_time]):
                return

        self._database.store_row_to_table("single_highscores", (level, time, initials))


    def is_challenge_score_eligible(self, score: int) -> bool:
        """Check if total score for completing a challenge game 
            is eligible for inclusion in high-score list.
            Only 5 highest scores will be stored.

        Args:
            score (int): Total score.

        Returns:
            bool: True if score can be included in high-score list.
        """
        # store high-score only if within 5 best
        current_highscores = self.get_challenge_highscores()

        if len(current_highscores) < 5:
            return True

        min_score = min(map(lambda x: x.score, current_highscores))
        if min_score < score:
            return True

        return False

    def store_challenge_highscore(self, score: int, initials: str):
        """Store challenge game total score with player initials as high-score.

        Args:
            score (int): Total score to store as a high-score result.
            initials (str): Player's initials to store for score.
        """
        if not self.is_challenge_score_eligible(score):
            return

        current_highscores = self.get_challenge_highscores()

        if len(current_highscores) >= 5:
            min_score = min(map(lambda x: x.score, current_highscores))
            if not self._database.remove_row_from_table("challenge_highscores",
                                                      ["score"],
                                                      [min_score]):
                return

        self._database.store_row_to_table("challenge_highscores", (score, initials))
