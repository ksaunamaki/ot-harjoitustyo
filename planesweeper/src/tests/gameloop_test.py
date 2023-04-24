import unittest
from loop import CoreLoop
from primitives.interfaces import Renderer, EventsCore
from primitives.game import GameInitialization, GameMode, GameState, ChallengeGameProgress
from primitives.state_transition import StateTransition
from entities.board import Gameboard, GameboardConfiguration
from services.database_service import DatabaseService


class TestCoreLoop(unittest.TestCase):
    def setUp(self):
        pass

    def test_single_game_initialization_state_transition(self):
        core_loop = CoreLoop(Renderer(), EventsCore(), DatabaseService())
        game_initialization: GameInitialization = GameInitialization(1, GameMode.SINGLE_GAME)

        transition: StateTransition = core_loop._initialize_new_game(game_initialization)

        self.assertEqual(transition.next, GameState.RUN_GAME)

        game: Gameboard = None
        progress: ChallengeGameProgress = None

        game_initialization, game, progress = transition.data

        self.assertEqual(game_initialization.level, 1)
        self.assertEqual(game_initialization.mode, GameMode.SINGLE_GAME)
        self.assertIsNone(game_initialization.ongoing_progress)

        self.assertEqual(game.get_level(), 1)
        self.assertIsNone(progress)


    def test_new_challenge_game_initialization_state_transition(self):
        core_loop = CoreLoop(Renderer(), EventsCore(), DatabaseService())
        game_initialization: GameInitialization = GameInitialization(1, GameMode.CHALLENGE_GAME)

        transition: StateTransition = core_loop._initialize_new_game(game_initialization)

        self.assertEqual(transition.next, GameState.RUN_GAME)

        game: Gameboard = None
        progress: ChallengeGameProgress = None

        game_initialization, game, progress = transition.data

        self.assertEqual(game_initialization.mode, GameMode.CHALLENGE_GAME)
        self.assertIsNone(game_initialization.ongoing_progress) # is set only after first round

        self.assertEqual(game.get_level(), 1)
        self.assertIsNotNone(progress)


    def test_continued_challenge_game_initialization_state_transition(self):
        core_loop = CoreLoop(Renderer(), EventsCore(), DatabaseService())
        ongoing_progress: ChallengeGameProgress = ChallengeGameProgress()
        ongoing_progress.current_level = 2
        game_initialization: GameInitialization = GameInitialization(1, GameMode.CHALLENGE_GAME, ongoing_progress)

        transition: StateTransition = core_loop._initialize_new_game(game_initialization)

        self.assertEqual(transition.next, GameState.RUN_GAME)

        game: Gameboard = None
        progress: ChallengeGameProgress = None

        game_initialization, game, progress = transition.data

        self.assertEqual(game_initialization.mode, GameMode.CHALLENGE_GAME)
        self.assertIsNotNone(game_initialization.ongoing_progress)

        self.assertEqual(game.get_level(), 2)
        self.assertIsNotNone(progress)


    def test_lost_challenge_game_level_decreases_score(self):
        core_loop = CoreLoop(Renderer(), EventsCore(), DatabaseService())
        game_initialization: GameInitialization = GameInitialization(1, GameMode.CHALLENGE_GAME)

        transition: StateTransition = core_loop._initialize_new_game(game_initialization)
        
        game: Gameboard = None
        progress: ChallengeGameProgress = None

        game_initialization, game, progress = transition.data

        self.assertIsNotNone(progress)

        progress.score = 1
        progress.last_won = False

        transition = core_loop._process_challenge_game_result(game, progress)

        # must remove one score
        self.assertEqual(progress.score, 0)
        # must increase level failures
        self.assertEqual(progress.level_failures, 1)


    def test_lost_challenge_game_level_score_not_negative(self):
        core_loop = CoreLoop(Renderer(), EventsCore(), DatabaseService())
        game_initialization: GameInitialization = GameInitialization(1, GameMode.CHALLENGE_GAME)

        transition: StateTransition = core_loop._initialize_new_game(game_initialization)
        
        game: Gameboard = None
        progress: ChallengeGameProgress = None

        game_initialization, game, progress = transition.data

        self.assertIsNotNone(progress)

        progress.score = 0
        progress.last_won = False

        transition = core_loop._process_challenge_game_result(game, progress)

        # score cannot be negative
        self.assertGreaterEqual(progress.score, 0)


    def test_lost_challenge_game_level1_maintains_level(self):
        core_loop = CoreLoop(Renderer(), EventsCore(), DatabaseService())
        game_initialization: GameInitialization = GameInitialization(1, GameMode.CHALLENGE_GAME)

        transition: StateTransition = core_loop._initialize_new_game(game_initialization)
        
        game: Gameboard = None
        progress: ChallengeGameProgress = None

        game_initialization, game, progress = transition.data

        self.assertIsNotNone(progress)

        progress.score = 25
        progress.level_failures = ((GameboardConfiguration.LEVELS[1][0][0] * GameboardConfiguration.LEVELS[1][0][1]) // 10) + 1
        progress.last_won = False

        transition = core_loop._process_challenge_game_result(game, progress)

        # must maintain level at 1
        self.assertEqual(progress.current_level, 1)


    def test_lost_challenge_game_level_downgrades_level(self):
        core_loop = CoreLoop(Renderer(), EventsCore(), DatabaseService())
        game_initialization: GameInitialization = GameInitialization(1, GameMode.CHALLENGE_GAME)

        transition: StateTransition = core_loop._initialize_new_game(game_initialization)
        
        game: Gameboard = None
        progress: ChallengeGameProgress = None

        game_initialization, game, progress = transition.data

        self.assertIsNotNone(progress)

        progress.score = 25
        progress.current_level = 2
        progress.level_failures = ((GameboardConfiguration.LEVELS[2][0][0] * GameboardConfiguration.LEVELS[2][0][1]) // 10) + 1
        progress.last_won = False

        transition = core_loop._process_challenge_game_result(game, progress)

        # must drop level to 1
        self.assertEqual(progress.current_level, 1)
        # must clear out level failures
        self.assertEqual(progress.level_failures, 0)

    def test_won_challenge_game_level_advances_level(self):
        core_loop = CoreLoop(Renderer(), EventsCore(), DatabaseService())
        game_initialization: GameInitialization = GameInitialization(1, GameMode.CHALLENGE_GAME)

        transition: StateTransition = core_loop._initialize_new_game(game_initialization)
        
        game: Gameboard = None
        progress: ChallengeGameProgress = None

        game_initialization, game, progress = transition.data

        self.assertIsNotNone(progress)

        progress.level_failures = 1
        progress.last_won = True

        transition = core_loop._process_challenge_game_result(game, progress)

        # must advance level to 2
        self.assertEqual(progress.current_level, 2)
        # must clear out level failures
        self.assertEqual(progress.level_failures, 0)
    
    def test_won_challenge_game_level_increases_score(self):
        core_loop = CoreLoop(Renderer(), EventsCore(), DatabaseService())
        game_initialization: GameInitialization = GameInitialization(1, GameMode.CHALLENGE_GAME)

        transition: StateTransition = core_loop._initialize_new_game(game_initialization)
        
        game: Gameboard = None
        progress: ChallengeGameProgress = None

        game_initialization, game, progress = transition.data

        self.assertIsNotNone(progress)

        progress.level_failures = 1
        progress.last_won = True

        transition = core_loop._process_challenge_game_result(game, progress)

        # must credit scores base on size of play area
        self.assertEqual(progress.score, game.get_pieces_on_board())
