from primitives.interfaces import RenderedObject, Renderer, EventsCore, EventType
from primitives.game_state import GameState
from primitives.game_initialization import GameInitialization
from primitives.state_transition import StateTransition
from entities.board import Gameboard
from entities.status_item import StatusItem
from entities.world_background import WorldBackground


class CoreLoop:
    def __init__(self, renderer: Renderer, events: EventsCore):
        self._renderer = renderer
        self._events = events
        self._background = WorldBackground()

    def _process_ui_events(self, game: Gameboard = None) -> StateTransition:

        # propage state transitions upstream if necessary

        while True:
            event, pos = self._events.get()

            if event == EventType.EXIT:
                return StateTransition(GameState.EXIT)

            if event == EventType.LEFT_CLICK:
                if game is None:
                    continue

                piece_position = game.translate_event_position_to_piece_position(
                    pos)

                if piece_position is None:
                    continue

                game.open_piece(piece_position)

            if event == EventType.RIGHT_CLICK:
                if game is None:
                    continue

                piece_position = game.translate_event_position_to_piece_position(
                    pos)

                if piece_position is None:
                    continue

                game.mark_piece(piece_position)

            if event == EventType.NEW_GAME:
                new_game: GameInitialization = None

                if game is not None:
                    new_game = GameInitialization(game.get_level())
                else:
                    new_game = GameInitialization(1)

                return StateTransition(GameState.INITIALIZE_NEW_GAME, new_game)

            if event == EventType.CHANGE_LEVEL_1:
                new_game: GameInitialization = GameInitialization(1)

                return StateTransition(GameState.INITIALIZE_NEW_GAME, new_game)

            if event == EventType.CHANGE_LEVEL_2:
                new_game: GameInitialization = GameInitialization(2)

                return StateTransition(GameState.INITIALIZE_NEW_GAME, new_game)

            if event == EventType.CHANGE_LEVEL_3:
                new_game: GameInitialization = GameInitialization(3)

                return StateTransition(GameState.INITIALIZE_NEW_GAME, new_game)

            if event == EventType.CHANGE_LEVEL_4:
                new_game: GameInitialization = GameInitialization(4)

                return StateTransition(GameState.INITIALIZE_NEW_GAME, new_game)

            if event == EventType.CHANGE_LEVEL_5:
                new_game: GameInitialization = GameInitialization(5)

                return StateTransition(GameState.INITIALIZE_NEW_GAME, new_game)

            if event == EventType.CHANGE_LEVEL_6:
                new_game: GameInitialization = GameInitialization(6)

                return StateTransition(GameState.INITIALIZE_NEW_GAME, new_game)

            if event == EventType.NONE:
                break

        return None

    def _run_initial(self) -> StateTransition:

        next_state: StateTransition = StateTransition(GameState.INITIAL)

        while True:
            # events
            transition = self._process_ui_events()

            if transition is not None:
                next_state = transition
                break

            # rendering
            self._renderer.compose([self._background])

            self._renderer.tick()

        return next_state

    def _render_game_ui(self, rendered_objects: list[RenderedObject],
                        game: Gameboard):
        # background
        rendered_objects.append(self._background)

        # game pieces
        for board_item in game.get_rendering_items():
            rendered_objects.append(board_item)

    def _render_status_bar(self, rendered_objects: list[RenderedObject],
                           state: GameState, game: Gameboard = None):
        if game is not None:
            radar_status = StatusItem(-5)
            radar_status.set_text(
                f"Radar contacts: {game.get_radar_contacts()} / {game.get_total_planes()}")

            rendered_objects.append(radar_status)

        if state == GameState.GAME_OVER:
            game_over_status = StatusItem(5)
            game_over_status.set_text(
                "GAME OVER! Press Alt+N to start new game with same level "
                    "or Alt+1 - Alt+6 to change level")

            rendered_objects.append(game_over_status)

    def _run_game(self, state: GameState, game: Gameboard) -> StateTransition:

        next_state: StateTransition = StateTransition(GameState.GAME_OVER)

        while True:
            # events
            transition = self._process_ui_events(game)

            if transition is not None:
                next_state = transition
                break

            # rendering
            rendered_objects: list[RenderedObject] = []

            self._render_game_ui(rendered_objects, game)
            self._render_status_bar(rendered_objects, state, game)

            self._renderer.compose(rendered_objects)

            # check for game end
            if state != GameState.GAME_OVER:
                game_result = game.game_end_result()

                if game_result is not None and game_result:
                    self._renderer.set_won_state()
                    break

                if game_result is not None and not game_result:
                    self._renderer.set_lost_state()
                    break

            self._renderer.tick()

        return next_state

    def _initialize_new_game(self,
            game_initialization: GameInitialization = None) -> StateTransition:

        next_state = GameState.SINGLE_GAME

        if game_initialization is None:
            # initialize new simple game board
            game = Gameboard(1)
            game.create()
        else:
            game = Gameboard(game_initialization.level)
            game.create()

            if not game_initialization.single_game:
                next_state = GameState.CHALLENGE_GAME

        self._background.position_board_on_world(game)

        return StateTransition(next_state, game)

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
            elif state in (GameState.SINGLE_GAME, GameState.CHALLENGE_GAME, GameState.GAME_OVER):
                transition = self._run_game(state, game)

            if transition is not None:
                state = transition.next

                if state in (GameState.SINGLE_GAME, GameState.CHALLENGE_GAME):
                    game = transition.data
                    self._renderer.set_game_state()
                elif state == GameState.INITIALIZE_NEW_GAME:
                    game_initialization = transition.data
                elif state == GameState.INITIAL:
                    self._renderer.set_game_state()
