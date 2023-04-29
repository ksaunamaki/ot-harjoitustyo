import unittest
import shutil, tempfile
from services.database_service import DatabaseService
from repositories.highscore_repository import HighScoreRepository


class TestHighscores(unittest.TestCase):
    def setUp(self):
        self._test_dir = tempfile.mkdtemp()
        self._database_service = DatabaseService(True, f"{self._test_dir}/TestHighscores")

    def tearDown(self):
        self._database_service.close()
        shutil.rmtree(self._test_dir)

    def test_new_single_highscore_is_stored(self):
        repository = HighScoreRepository(self._database_service)

        self.assertEqual(len(repository.get_single_highscores(1)), 0)

        repository.store_single_highscore(1, 5, "TST")
        
        self.assertEqual(len(repository.get_single_highscores(1)), 1)

    def test_new_single_highscore_levels_not_mixed(self):
        repository = HighScoreRepository(self._database_service)

        repository.store_single_highscore(1, 5, "ABC")
        repository.store_single_highscore(2, 5, "XYZ")

        level_1_scores = repository.get_single_highscores(1)
        
        self.assertEqual(len(level_1_scores), 1)
        self.assertEqual(level_1_scores[0].initials, "ABC")

    def test_new_single_highscore_replaces_largest_existing(self):
        repository = HighScoreRepository(self._database_service)

        repository.store_single_highscore(1, 1, "TST1")
        repository.store_single_highscore(1, 2, "TST2")
        repository.store_single_highscore(1, 3, "TST3")
        repository.store_single_highscore(1, 4, "TST4")
        repository.store_single_highscore(1, 5, "TST5")

        repository.store_single_highscore(1, 2.5, "TST2.5")

        level_1_scores = repository.get_single_highscores(1)

        for highscore in level_1_scores:
            self.assertNotEqual(highscore.initials, "TST5")
            self.assertNotAlmostEqual(highscore.time, 5, 1)
    
    def test_new_single_out_of_bounds_highscore_not_replace_existing(self):
        repository = HighScoreRepository(self._database_service)

        repository.store_single_highscore(1, 1, "TST1")
        repository.store_single_highscore(1, 2, "TST2")
        repository.store_single_highscore(1, 3, "TST3")
        repository.store_single_highscore(1, 4, "TST4")
        repository.store_single_highscore(1, 5, "TST5")

        repository.store_single_highscore(1, 6, "TST6")

        level_1_scores = repository.get_single_highscores(1)

        for highscore in level_1_scores:
            self.assertNotEqual(highscore.initials, "TST6")
            self.assertNotAlmostEqual(highscore.time, 6, 1)

    def test_new_challenge_highscore_is_stored(self):
        repository = HighScoreRepository(self._database_service)

        self.assertEqual(len(repository.get_challenge_highscores()), 0)

        repository.store_challenge_highscore(500, "TST")
        
        self.assertEqual(len(repository.get_challenge_highscores()), 1)

    def test_new_challenge_highscore_replaces_largest_existing(self):
        repository = HighScoreRepository(self._database_service)

        repository.store_challenge_highscore(100, "TST1")
        repository.store_challenge_highscore(200, "TST2")
        repository.store_challenge_highscore(300, "TST3")
        repository.store_challenge_highscore(400, "TST4")
        repository.store_challenge_highscore(500, "TST5")

        repository.store_challenge_highscore(600, "TST6")

        scores = repository.get_challenge_highscores()

        for highscore in scores:
            self.assertNotEqual(highscore.initials, "TST1")
            self.assertNotEqual(highscore.score, 100)
    
    def test_new_challenge_out_of_bounds_highscore_not_replace_existing(self):
        repository = HighScoreRepository(self._database_service)

        repository.store_challenge_highscore(100, "TST1")
        repository.store_challenge_highscore(200, "TST2")
        repository.store_challenge_highscore(300, "TST3")
        repository.store_challenge_highscore(400, "TST4")
        repository.store_challenge_highscore(500, "TST5")

        repository.store_challenge_highscore(50, "TST6")

        scores = repository.get_challenge_highscores()

        for highscore in scores:
            self.assertNotEqual(highscore.initials, "TST6")
            self.assertNotEqual(highscore.score, 50)
