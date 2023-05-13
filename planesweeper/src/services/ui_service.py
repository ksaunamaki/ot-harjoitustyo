from entities.board import Gameboard, BoardState
from entities.ui.text_overlay import TextOverlay
from entities.ui.button import Button
from entities.ui.status_item import StatusItem
from primitives.interfaces import RenderedObject, Renderer
from primitives.game import GameMode, GameInitialization, GameState, ChallengeGameProgress
from primitives.position import Position
from primitives.size import Size
from primitives.color import Color
from primitives.border import Border
from primitives.events import EventData, EventType
from services.language_service import LanguageService
from repositories.highscore_repository import HighScoreRepository


class UiService:
    """Creates UI elements to render on game UI.
    """

    def __init__(self,
                 renderer: Renderer,
                 highscores: HighScoreRepository,
                 language_service: LanguageService):
        self._renderer = renderer
        self._highscores = highscores
        self._language_service = language_service

    def _get_formatted_play_time(self, total_time: float) -> str:
        minutes = int(total_time // 60)
        seconds = int(total_time % 60)

        return f"{minutes:02d}:{seconds:02d}"

    def _get_high_scores_text(self,
                              game_initialization: GameInitialization) -> str:
        text = ""

        if game_initialization.mode == GameMode.SINGLE_GAME:
            high_scores = self._highscores.get_single_highscores(game_initialization.level)

            if len(high_scores) > 0:
                text += f" {self._language_service.get_text('current_best_times')}:"

            for score in high_scores:
                text += f"  {self._get_formatted_play_time(score.time)} by {score.initials}"
        else:
            high_scores = self._highscores.get_challenge_highscores()

            if len(high_scores) > 0:
                text += f" {self._language_service.get_text('current_high_scores')}:"

            for score in high_scores:
                txt = self._language_service.get_text("points_by",
                                                      [score.score,score.initials])
                text += f" {txt}"

        return text

    def create_game_over_overlay(self,
                                 game_state: BoardState,
                                 game_initialization: GameInitialization) -> TextOverlay:
        """Creates game over -text overlay.

        Args:
            game_state (BoardState): Current state of the gameboard
            game_initialization (GameInitialization): Current game initialization data

        Returns:
            TextOverlay: Created overlay object
        """
        game_over_text = ""

        if game_state == BoardState.WON:
            game_over_text = self._language_service.get_text("game_won") +\
                self._get_high_scores_text(game_initialization)
        else:
            game_over_text = self._language_service.get_text("game_lost") +\
                self._get_high_scores_text(game_initialization)

        overlay = TextOverlay(game_over_text, 14, Position(5,10), Color(255,255,255),
                            Position(0,15), Size(self._renderer.WINDOW_WIDTH, 35),
                            Color(0,0,0), None, self._renderer)

        return overlay

    def create_initials_overlay(self) -> TextOverlay:
        """Creates user's initials -text overlay for high-score inital input.

        Returns:
            TextOverlay: Created overlay object
        """
        text = f"{self._language_service.get_text('enter_initials')}: "

        overlay = TextOverlay(text, 30,
                              Position(5, 15),
                              Color(255,255,255),
                              Position(20,self._renderer.get_play_area_size().height // 2 - 30),
                              Size(self._renderer.WINDOW_WIDTH - 40, 60),
                              Color(19,146,119,0.5), None, self._renderer)
        overlay.enable_blink_on_end()

        return overlay

    def create_challenge_advance_overlay(self) -> TextOverlay:
        """Creates advance to next level - text overlay for challenge game.

        Returns:
            TextOverlay: Created overlay object
        """
        text = self._language_service.get_text("challenge_level_cleared")

        overlay = TextOverlay(text, 14, Position(10,10), Color(255,255,255),
                            Position(0,15), Size(self._renderer.WINDOW_WIDTH, 35),
                            Color(20,147,92, 0.7), None, self._renderer)

        return overlay

    def create_challenge_level_try_again_overlay(self, score: int) -> TextOverlay:
        """Creates try again -text overlay for challenge game.

        Args:
            score (int): Current challenge game score

        Returns:
            TextOverlay: Created overlay object
        """
        text = f"{self._language_service.get_text('challenge_try_again')} "

        if score > 0:
            text += self._language_service.get_text("challenge_point_lost")
        else:
            text += self._language_service.get_text("challenge_keep_trying")

        overlay = TextOverlay(text, 14, Position(10,10), Color(255,255,255),
                            Position(0,15), Size(self._renderer.WINDOW_WIDTH, 35),
                            Color(207,65,3, 0.7), None, self._renderer)

        return overlay

    def create_challenge_downgrade_try_again_overlay(self) -> TextOverlay:
        """Creates level downgraded -text overlay for challenge game.

        Returns:
            TextOverlay: Created overlay object
        """
        text = f"{self._language_service.get_text('challenge_try_again')} "
        text += self._language_service.get_text("challenge_level_downgrade")

        overlay = TextOverlay(text, 14, Position(10,10), Color(255,255,255),
                            Position(0,15), Size(self._renderer.WINDOW_WIDTH, 35),
                            Color(207,65,3, 0.7), None, self._renderer)

        return overlay

    def create_game_selection_buttons(self) -> dict:
        """Creates game mode selection buttons for initial screen.

        Returns:
            dict: Dictionary of button objects with names as key.
        """
        buttons = {}

        pos_y = self._renderer.get_play_area_size().height // 8

        border =  Border(Color(0,0,0), 1)

        text_single = self._language_service.get_text("start_single_game")

        single_game_buttons = Button(text_single, 20,
                              Position(50, 10),
                              Color(0,0,0),
                              Position(100, pos_y * 3),
                              Size(self._renderer.WINDOW_WIDTH - 200, 40),
                              Color(255,255,255,0.95), border,
                              EventData(EventType.NEW_SINGLE_GAME),
                              self._renderer)

        text_challenge = self._language_service.get_text("start_challenge_game")

        challenge_game_button = Button(text_challenge, 20,
                              Position(100, 10),
                              Color(0,0,0),
                              Position(100, pos_y * 4),
                              Size(self._renderer.WINDOW_WIDTH - 200, 40),
                              Color(255,255,255,0.95), border,
                              EventData(EventType.NEW_CHALLENGE_GAME),
                              self._renderer)

        buttons["single_game_button"] = single_game_buttons
        buttons["challenge_game_button"] = challenge_game_button

        return buttons

    def render_gameboard(self,
                       rendered_objects: list[RenderedObject],
                       game: Gameboard):
        """Creates main gameboard UI elements.

        Args:
            rendered_objects (list[RenderedObject]):
                Main list of rendered objects for which UI elements are added to.
            game (Gameboard): Current gameboard object.
        """
        for board_item in game.get_rendering_items():
            rendered_objects.append(board_item)

    def render_status_bar(self, rendered_objects: list[RenderedObject],
                           state: GameState,
                           game: Gameboard = None,
                           progress: ChallengeGameProgress = None):
        """Creates status bar UI elements.

        Args:
            rendered_objects (list[RenderedObject]):
                Main list of rendered objects for which UI elements are added to.
            state (GameState): Current game state object.
            game (Gameboard, optional): Current gameboard object. 
                None if no gameboard is shown on screen.
            progress (ChallengeGameProgress, optional): Current challenge game tracking data.
                None if no challenge game is shown on screen.
        """
        if game is not None:
            radar_text = self._language_service.get_text("status_radar_contacts",
                                                         [game.get_radar_contacts(),
                                                          game.get_total_planes()])
            radar_status = StatusItem(radar_text, -5, True, self._renderer)

            rendered_objects.append(radar_status)

            progress_text = ""

            if progress is None:
                elapsed = game.get_elapsed_play_time()
                progress_text = self._language_service.get_text("status_playtime",
                                                    [self._get_formatted_play_time(elapsed)])
            else:
                progress_text = self._language_service.get_text("status_score",
                                                                [progress.score])

            progress_status = StatusItem(progress_text, 5, False, self._renderer)

            rendered_objects.append(progress_status)

        if state != GameState.RUN_GAME:
            new_game_text = self._language_service.get_text("status_new_game")
            new_game_status = StatusItem(
                new_game_text,
                0,
                True,
                self._renderer)

            # reposition to middle based on actual text size
            text_object = new_game_status.get_text()
            new_position = Position(
                self._renderer.get_status_area_size().width // 2 -\
                    (self._renderer.measure_text_dimensions(text_object).width // 2),
                new_game_status.get_position().y)
            new_game_status.change_position(new_position)

            rendered_objects.append(new_game_status)
