from primitives.interfaces import RenderedObject, Renderer, EventsCore
from primitives.game_state import GameState
from primitives.game_mode import GameMode
from primitives.game_initialization import GameInitialization
from primitives.state_transition import StateTransition
from primitives.position import Position
from primitives.size import Size
from primitives.color import Color
from entities.board import Gameboard, BoardState
from entities.ui.status_item import StatusItem
from entities.ui.text_overlay import TextOverlay
from entities.ui.world_background import WorldBackground
from repositories.highscore_repository import HighScoreRepository
from services.events_handling_service import EventsHandlingService, InputBuffer
from services.database_service import DatabaseService


class CoreLoop:
    def __init__(self, renderer: Renderer, events: EventsCore, database: DatabaseService):
        self._renderer = renderer
        self._highscores = HighScoreRepository(database)
        self._long_lived_elements = {}
        self.events_handler = EventsHandlingService(events)

        background = WorldBackground(renderer)
        self._long_lived_elements["background"] = background

    def _render_long_lasting_elements(self, rendered_objects: list[RenderedObject]):
        for element in self._long_lived_elements.values():
            rendered_objects.append(element)

    def _render_game_ui(self, rendered_objects: list[RenderedObject],
                        game: Gameboard):
        # game pieces
        for board_item in game.get_rendering_items():
            rendered_objects.append(board_item)

    def _get_formatted_play_time(self, time: float) -> str:
        minutes = int(time // 60)
        seconds = int(time % 60)

        return f"{minutes:02d}:{seconds:02d}"

    def _get_high_scores(self, game_initialization: GameInitialization) -> str:
        text = ""

        if game_initialization.mode == GameMode.SINGLE_GAME:
            high_scores = self._highscores.get_single_highscores(game_initialization.level)

            if len(high_scores) > 0:
                text += " Current best times:"

            for score in high_scores:
                text += f"  {self._get_formatted_play_time(score.time)} by {score.initials}"
        else:
            high_scores = self._highscores.get_challenge_highscores()

            if len(high_scores) > 0:
                text += " Current high scores:"

            for score in high_scores:
                text += f" {score.score} points by {score.initials}"

        return text

    def _create_game_over_overlay(self,
                                  game_state: BoardState,
                                  game_initialization: GameInitialization):
        game_over_text = ""

        if game_state == BoardState.WON:
            game_over_text = "Congratulations, you won the game!" +\
                self._get_high_scores(game_initialization)
        else:
            game_over_text = "Better luck next time!" +\
                self._get_high_scores(game_initialization)

        overlay = TextOverlay(game_over_text, 14, Position(5,10), Color(255,255,255),
                            Position(0,15), Size(self._renderer.WINDOW_WIDTH, 35),
                            Color(0,0,0), self._renderer)

        self._long_lived_elements["game_over_overlay"] = overlay

    def _create_initials_overlay(self):
        text = "Please enter your initials for high-score board: "

        overlay = TextOverlay(text, 30,
                              Position(5, 15),
                              Color(255,255,255),
                              Position(20,self._renderer.get_play_area_size().height // 2 - 30),
                              Size(self._renderer.WINDOW_WIDTH - 40, 60),
                              Color(19,146,119,0.5), self._renderer)
        overlay.enable_blink_on_end()

        self._long_lived_elements["initials_overlay"] = overlay

    def _render_overlays(self,
                         state: GameState,
                         game_initialization: GameInitialization,
                         game: Gameboard = None):
        game_state = game.get_current_board_state()

        if state == GameState.GAME_OVER:
            if "game_over_overlay" not in self._long_lived_elements:
                self._create_game_over_overlay(game_state, game_initialization)
            else:
                overlay = self._long_lived_elements["game_over_overlay"]
                overlay.tick()

        if state == GameState.GET_INITIALS:
            if "initials_overlay" not in self._long_lived_elements:
                self._create_initials_overlay()
            else:
                overlay = self._long_lived_elements["initials_overlay"]
                overlay.tick()

    def _render_status_bar(self, rendered_objects: list[RenderedObject],
                           state: GameState,
                           game: Gameboard = None):
        if game is not None:
            radar_text = f"Radar contacts: {game.get_radar_contacts()} / {game.get_total_planes()}"
            radar_status = StatusItem(radar_text, -5, True, self._renderer)

            rendered_objects.append(radar_status)

            elapsed_text = f"Time: {self._get_formatted_play_time(game.get_elapsed_play_time())}"
            elapsed_status = StatusItem(elapsed_text, 5, False, self._renderer)

            rendered_objects.append(elapsed_status)

        if state != GameState.RUN_GAME:
            new_game_text = " Press Alt+N or Alt+[1-6] to start a new game"
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

    def _run_initial(self) -> StateTransition:

        transition: StateTransition = None

        while True:
            # events
            transition = self.events_handler.process_events(GameState.INITIAL, None, None)

            if transition is not None:
                break

            # rendering
            rendered_objects: list[RenderedObject] = []
            self._render_long_lasting_elements(rendered_objects)
            self._render_status_bar(rendered_objects, GameState.INITIAL)

            self._renderer.compose(rendered_objects)

            self._renderer.tick()

        return transition

    def _check_if_game_has_ended(self,
                                 game_initialization: GameInitialization,
                                 game: Gameboard) -> StateTransition:
        game_result = game.get_current_board_state()
        transition: StateTransition = None

        if game_result == BoardState.WON:
            self._renderer.set_won_state()

            transition = StateTransition(GameState.GAME_OVER)

            if game_initialization.mode == GameMode.SINGLE_GAME:
                if self._highscores.is_single_score_eligible(
                    game_initialization.level,
                    game.get_elapsed_play_time()):
                    transition = StateTransition(GameState.GET_INITIALS)

        if game_result == BoardState.LOST:
            self._renderer.set_lost_state()
            transition = StateTransition(GameState.GAME_OVER)

        return transition

    def _run_game(self,
                  state: GameState,
                  game_initialization: GameInitialization,
                  game: Gameboard) -> StateTransition:

        transition: StateTransition = None

        while True:
            # events
            transition = self.events_handler.process_events(state, game_initialization, game)

            # check for game end
            if transition is None and state != GameState.GAME_OVER:
                transition = self._check_if_game_has_ended(game_initialization, game)

            if transition is not None:
                break

            # rendering
            rendered_objects: list[RenderedObject] = []

            self._render_long_lasting_elements(rendered_objects)
            self._render_game_ui(rendered_objects, game)
            self._render_status_bar(rendered_objects, state, game)
            self._render_overlays(state, game_initialization, game)

            self._renderer.compose(rendered_objects)

            self._renderer.tick()

        return transition

    def _handle_initials_input(self,
                               input_buffer: InputBuffer,
                               initials: str,
                               game_initialization: GameInitialization,
                               game: Gameboard) -> tuple[str, StateTransition]:
        transition = None
        data = "".join(map(lambda c: c.upper(), input_buffer.read()))

        is_backspace = data == '\x08'

        if not is_backspace:
            max_left = 3 - min(len(initials), 3)

            if len(data) > max_left:
                data = data[0:max_left]

        overlay: TextOverlay = self._long_lived_elements["initials_overlay"]

        if not is_backspace:
            overlay.append_text(data)
            initials += data
        else:
            if len(initials) > 0:
                overlay.truncate_text(1)
                initials = initials[0:-1]

        if len(initials) >= 3:
            initials = initials[0:3]
            self._highscores.store_single_highscore(
                game_initialization.level,
                game.get_elapsed_play_time(),
                initials)

            transition = StateTransition(GameState.GAME_OVER)

        return (initials, transition)

    def _run_get_initials(self,
                  state: GameState,
                  game_initialization: GameInitialization,
                  game: Gameboard) -> StateTransition:

        transition: StateTransition = None
        initials = ""
        input_buffer = InputBuffer()

        while True:
            # events
            transition = self.events_handler.process_events(
                state,
                game_initialization, game,
                input_buffer)

            if transition is None and input_buffer.is_updated:
                initials, transition = self._handle_initials_input(
                    input_buffer,
                    initials,
                    game_initialization,
                    game)

            if transition is not None:
                break

            # rendering
            rendered_objects: list[RenderedObject] = []

            self._render_long_lasting_elements(rendered_objects)
            self._render_game_ui(rendered_objects, game)
            self._render_status_bar(rendered_objects, state, game)
            self._render_overlays(state, game_initialization, game)

            self._renderer.compose(rendered_objects)

            self._renderer.tick()

        # remove overlay
        self._long_lived_elements.pop("initials_overlay", None)

        return transition

    def _initialize_new_game(self,
            game_initialization: GameInitialization = None) -> StateTransition:

        next_state = GameState.RUN_GAME

        if game_initialization is None:
            # initialize new simple game board
            game = Gameboard(1)
            game.create()
        else:
            game = Gameboard(game_initialization.level)
            game.create()

        self._long_lived_elements["background"].position_board_on_world(game)

        # remove game over text if is shown
        self._long_lived_elements.pop("game_over_overlay", None)

        return StateTransition(next_state, (game_initialization, game))

    def _process_transition(self,
                            transition: StateTransition,
                            game_initialization: GameInitialization,
                            game: Gameboard) -> tuple[GameState, GameInitialization, Gameboard]:
        state = transition.next

        if state == GameState.RUN_GAME:
            game_initialization = transition.data[0]
            game = transition.data[1]
            self._renderer.set_game_state()
        elif state == GameState.INITIALIZE_NEW_GAME:
            game_initialization = transition.data
        elif state == GameState.INITIAL:
            self._renderer.set_game_state()

        return (state, game_initialization, game)

    def run(self,
            state: GameState = GameState.INITIAL,
            game_initialization: GameInitialization = None) -> bool:

        game: Gameboard = None

        while state != GameState.EXIT:

            transition: StateTransition = None

            if state == GameState.INITIAL:
                transition = self._run_initial()
            elif state == GameState.INITIALIZE_NEW_GAME:
                transition = self._initialize_new_game(game_initialization)
            elif state in (GameState.RUN_GAME, GameState.GAME_OVER):
                transition = self._run_game(state, game_initialization, game)
            elif state == GameState.GET_INITIALS:
                transition = self._run_get_initials(state, game_initialization, game)

            if transition is not None:
                state, game_initialization, game = self._process_transition(
                    transition,
                    game_initialization,
                    game)
