import time
from primitives.interfaces import RenderedObject, Renderer, EventsCore
from primitives.game import GameState, GameMode, GameInitialization, ChallengeGameProgress
from primitives.state_transition import StateTransition
from entities.board import Gameboard, BoardState, GameboardConfiguration
from entities.ui.text_overlay import TextOverlay
from entities.ui.world_background import WorldBackground
from repositories.highscore_repository import HighScoreRepository
from services.events_handling_service import EventsHandlingService, InputBuffer
from services.language_service import LanguageService
from services.ui_service import UiService


class CoreLoop:
    def __init__(self,
                 highscores: HighScoreRepository,
                 renderer: Renderer,
                 events: EventsCore,
                 language_service: LanguageService):
        self._highscores = highscores
        self._renderer = renderer
        self._long_lived_elements = {}
        self._events_handler = EventsHandlingService(events, renderer)
        self._language_service = language_service
        self._ui_service = UiService(renderer, highscores, language_service)

        background = WorldBackground(renderer)
        self._long_lived_elements["background"] = background

    def _render_long_lived_elements(self, rendered_objects: list[RenderedObject]):
        for element in self._long_lived_elements.values():
            rendered_objects.append(element)

    def _render_overlays(self,
                         state: GameState,
                         game_initialization: GameInitialization,
                         game: Gameboard,
                         progress: ChallengeGameProgress = None):
        game_state = game.get_current_board_state() if game is not None else None

        if state == GameState.GAME_OVER:
            if "game_over_overlay" not in self._long_lived_elements:
                self._long_lived_elements["game_over_overlay"] = \
                    self._ui_service.create_game_over_overlay(game_state, game_initialization)

            overlay = self._long_lived_elements["game_over_overlay"]
            overlay.tick()

        if state == GameState.GET_INITIALS:
            if "initials_overlay" not in self._long_lived_elements:
                self._long_lived_elements["initials_overlay"] = \
                    self._ui_service.create_initials_overlay()

            overlay = self._long_lived_elements["initials_overlay"]
            overlay.tick()

        if progress is not None:
            if "challenge_overlay" in self._long_lived_elements:
                overlay = self._long_lived_elements["challenge_overlay"]
                overlay.tick()

                if (time.time() - progress.message_shown_start) > 10:
                    # remove overlay after timeout to avoid obscuring play area
                    self._long_lived_elements.pop("challenge_overlay", None)

    def _run_initial(self) -> StateTransition:

        transition: StateTransition = None
        state = GameState.INITIAL

        buttons = self._ui_service.create_game_selection_buttons()

        for key, overlay in buttons.items():
            self._long_lived_elements[key] = overlay

        while True:
            # events
            transition = self._events_handler.process_events(
                state,
                None,
                None,
                buttons.values())

            if transition is not None:
                break

            # rendering
            rendered_objects: list[RenderedObject] = []
            self._render_long_lived_elements(rendered_objects)
            self._renderer.compose(rendered_objects)

            self._renderer.tick()

        # remove buttons
        for key, _ in buttons.items():
            self._long_lived_elements.pop(key, None)

        return transition

    def _check_if_game_has_ended(self,
                                 game_initialization: GameInitialization,
                                 game: Gameboard,
                                 progress: ChallengeGameProgress) -> StateTransition:
        game_result = game.get_current_board_state()
        transition: StateTransition = None

        if game_result == BoardState.WON:
            if game_initialization.mode == GameMode.SINGLE_GAME:
                self._renderer.set_won_state()
                transition = StateTransition(GameState.GAME_OVER)
                if self._highscores.is_single_score_eligible(
                    game_initialization.level,
                    game.get_elapsed_play_time()):
                    transition = StateTransition(GameState.GET_INITIALS)
            else:
                progress.last_won = True
                transition = StateTransition(GameState.PROCESS_CHALLENGE_ROUND_RESULT)

        if game_result == BoardState.LOST:
            if game_initialization.mode == GameMode.SINGLE_GAME:
                self._renderer.set_lost_state()
                transition = StateTransition(GameState.GAME_OVER)
            else:
                progress.last_won = False
                transition = StateTransition(GameState.PROCESS_CHALLENGE_ROUND_RESULT)

        return transition

    def _run_game(self,
                  state: GameState,
                  game_initialization: GameInitialization,
                  game: Gameboard,
                  progress: ChallengeGameProgress) -> StateTransition:

        transition: StateTransition = None

        while True:
            # events
            transition = self._events_handler.process_events(
                state,
                game_initialization,
                game)

            # check for game end
            if transition is None and state != GameState.GAME_OVER:
                transition = self._check_if_game_has_ended(
                    game_initialization,
                    game,
                    progress)

            if transition is not None:
                break

            # rendering
            rendered_objects: list[RenderedObject] = []

            self._render_long_lived_elements(rendered_objects)
            self._ui_service.render_gameboard(rendered_objects, game)
            self._ui_service.render_status_bar(rendered_objects, state, game, progress)
            self._render_overlays(state, game_initialization, game, progress)

            self._renderer.compose(rendered_objects)

            self._renderer.tick()

        return transition

    def _store_initials(self,
                        initials: str,
                        game_initialization: GameInitialization,
                        game: Gameboard,
                        progress: ChallengeGameProgress) -> tuple[str, StateTransition]:
        initials = initials[0:3]

        if progress is None:
            self._highscores.store_single_highscore(
                game_initialization.level,
                game.get_elapsed_play_time(),
                initials)
        else:
            self._highscores.store_challenge_highscore(
                progress.score,
                initials)

        return StateTransition(GameState.GAME_OVER)

    def _handle_initials_input(self,
                               input_buffer: InputBuffer,
                               initials: str,
                               game_initialization: GameInitialization,
                               game: Gameboard,
                               progress: ChallengeGameProgress) -> tuple[str, StateTransition]:
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
            transition = self._store_initials(initials, game_initialization, game, progress)

        return (initials, transition)

    def _run_get_initials(self,
                  state: GameState,
                  game_initialization: GameInitialization,
                  game: Gameboard,
                  progress: ChallengeGameProgress) -> StateTransition:

        transition: StateTransition = None
        initials = ""
        input_buffer = InputBuffer()

        while True:
            # events
            transition = self._events_handler.process_events(
                state,
                game_initialization,
                game,
                None,
                input_buffer)

            if transition is None and input_buffer.is_updated:
                initials, transition = self._handle_initials_input(
                    input_buffer,
                    initials,
                    game_initialization,
                    game,
                    progress)

            if transition is not None:
                break

            # rendering
            rendered_objects: list[RenderedObject] = []

            self._render_long_lived_elements(rendered_objects)
            self._ui_service.render_gameboard(rendered_objects, game)
            self._ui_service.render_status_bar(rendered_objects, state, game)
            self._render_overlays(state, game_initialization, game)

            self._renderer.compose(rendered_objects)

            self._renderer.tick()

        # remove overlay
        self._long_lived_elements.pop("initials_overlay", None)

        return transition

    def _initialize_new_game(self,
                    game_initialization: GameInitialization = None) -> StateTransition:

        progress: ChallengeGameProgress = None

        if game_initialization is None:
            # initialize new simple game board
            game_initialization = GameInitialization(1)

        if game_initialization.mode == GameMode.SINGLE_GAME:
            game = Gameboard(game_initialization.level)
            game.create()
        else:
            if game_initialization.ongoing_progress is None:
                progress = ChallengeGameProgress()
                game = Gameboard(1)
            else:
                progress = game_initialization.ongoing_progress
                game = Gameboard(progress.current_level)

            game.create()

        self._long_lived_elements["background"].position_board_on_world(game)

        # remove game over text if is shown
        self._long_lived_elements.pop("game_over_overlay", None)

        if game_initialization.ongoing_progress is None:
            self._long_lived_elements.pop("challenge_overlay", None)

        return StateTransition(GameState.RUN_GAME,
                               (game_initialization, game, progress))

    def _challenge_game_over(self,
                             progress: ChallengeGameProgress) -> StateTransition:
        self._renderer.set_won_state()
        transition = StateTransition(GameState.GAME_OVER)

        if self._highscores.is_challenge_score_eligible(progress.score):
            transition = StateTransition(GameState.GET_INITIALS)

        return transition

    def _process_challenge_game_result(self,
                                 game: Gameboard,
                                 progress: ChallengeGameProgress) -> StateTransition:
        self._long_lived_elements.pop("try_again_overlay", None)

        solved_game_size = game.get_pieces_on_board()

        if progress.last_won:
            progress.current_level = progress.current_level + 1
            progress.score += solved_game_size

            progress.level_failures = 0

            if progress.current_level >= GameboardConfiguration.get_max_level()+1:
                return self._challenge_game_over(progress)

            self._long_lived_elements["challenge_overlay"] = \
                self._ui_service.create_challenge_advance_overlay()
        else:
            progress.level_failures += 1
            progress.score = max(0, progress.score - 1)

            # if failing more times than there's 10% of pieces on the current board
            # then drop to previous level (except for the first level)
            if progress.current_level > 1 and\
                    progress.level_failures > solved_game_size // 10:
                progress.current_level = progress.current_level - 1
                progress.level_failures = 0

                self._long_lived_elements["challenge_overlay"] = \
                    self._ui_service.create_challenge_downgrade_try_again_overlay()
            else:
                self._long_lived_elements["challenge_overlay"] = \
                    self._ui_service.create_challenge_level_try_again_overlay(progress.score)

        progress.message_shown_start = time.time()

        # initialize new game round
        return StateTransition(GameState.INITIALIZE_NEW_GAME,
                               GameInitialization(progress.current_level,
                                                  GameMode.CHALLENGE_GAME,
                                                  progress))

    def _process_transition(self,
                            transition: StateTransition,
                            game_initialization: GameInitialization,
                            game: Gameboard,
                            progress: ChallengeGameProgress)\
                        -> tuple[GameState, GameInitialization, Gameboard, ChallengeGameProgress]:
        state = transition.next

        if state == GameState.RUN_GAME:
            game_initialization = transition.data[0]
            game = transition.data[1]
            progress = transition.data[2]
            self._renderer.set_game_state()
        elif state == GameState.INITIALIZE_NEW_GAME:
            game_initialization = transition.data
        elif state == GameState.INITIAL:
            self._renderer.set_game_state()

        return (state, game_initialization, game, progress)

    def run(self) -> bool:

        game: Gameboard = None
        game_initialization: GameInitialization = None
        state: GameState = GameState.INITIAL
        progress: ChallengeGameProgress = None

        while state != GameState.EXIT:

            transition: StateTransition = None

            if state == GameState.INITIAL:
                transition = self._run_initial()
            elif state == GameState.INITIALIZE_NEW_GAME:
                transition = self._initialize_new_game(game_initialization)
            elif state in (GameState.RUN_GAME, GameState.GAME_OVER):
                transition = self._run_game(state, game_initialization, game, progress)
            elif state == GameState.GET_INITIALS:
                transition = self._run_get_initials(state, game_initialization, game, progress)
            elif state == GameState.PROCESS_CHALLENGE_ROUND_RESULT:
                transition = self._process_challenge_game_result(game, progress)

            if transition is not None:
                state, game_initialization, game, progress = self._process_transition(
                    transition,
                    game_initialization,
                    game,
                    progress)
