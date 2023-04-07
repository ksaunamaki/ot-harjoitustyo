from primitives.interfaces import RenderedObject, Renderer, EventsCore
from primitives.game_state import GameState
from primitives.game_initialization import GameInitialization
from primitives.state_transition import StateTransition
from entities.board import Gameboard, BoardState
from entities.ui.status_item import StatusItem
from entities.ui.world_background import WorldBackground
from services.events_handling_service import EventsHandlingService


class CoreLoop:
    def __init__(self, renderer: Renderer, events: EventsCore):
        self._renderer = renderer
        self._background = WorldBackground(renderer)
        self.events_handler = EventsHandlingService(events)

    def _run_initial(self) -> StateTransition:

        next_state: StateTransition = StateTransition(GameState.INITIAL)

        while True:
            # events
            transition = self.events_handler.process_events(None)

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
            radar_text = f"Radar contacts: {game.get_radar_contacts()} / {game.get_total_planes()}"
            radar_status = StatusItem(radar_text, -5, True, self._renderer)

            rendered_objects.append(radar_status)

        if state == GameState.GAME_OVER:
            game_over_text = "GAME OVER! Press Alt+N to start new game with same level "\
                    "or Alt+1 - Alt+6 to change level"
            game_over_status = StatusItem(game_over_text, 5, False, self._renderer)

            rendered_objects.append(game_over_status)

    def _run_game(self, state: GameState, game: Gameboard) -> StateTransition:

        next_state: StateTransition = StateTransition(GameState.GAME_OVER)

        while True:
            # events
            transition = self.events_handler.process_events(game)

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
                game_result = game.get_current_board_state()

                if game_result == BoardState.WON:
                    self._renderer.set_won_state()
                    break

                if game_result == BoardState.LOST:
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
