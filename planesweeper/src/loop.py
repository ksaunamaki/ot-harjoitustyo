from primitives.interfaces import RenderedObject,Renderer,EventsCore,EventType
from primitives.interfaces import EventsCore,EventType
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
                return StateTransition(GameState.Exit)
            
            if event == EventType.LEFT_CLICK:
                if game == None:
                    continue

                piece_position = game.translate_event_position_to_piece_position(pos)

                if piece_position == None:
                    continue

                game.open_piece(piece_position)

            if event == EventType.RIGHT_CLICK:
                if game == None:
                    continue

                piece_position = game.translate_event_position_to_piece_position(pos)

                if piece_position == None:
                    continue

                game.mark_piece(piece_position)

            if event == EventType.NEW_GAME:
                newGame: GameInitialization = None

                if game != None:
                    newGame = GameInitialization(game.get_level())
                else:
                    newGame = GameInitialization(1)

                return StateTransition(GameState.InitializeNewGame, newGame)
            
            if event == EventType.CHANGE_LEVEL_1:
                newGame: GameInitialization = GameInitialization(1)

                return StateTransition(GameState.InitializeNewGame, newGame)
            
            if event == EventType.CHANGE_LEVEL_2:
                newGame: GameInitialization = GameInitialization(2)

                return StateTransition(GameState.InitializeNewGame, newGame)
            
            if event == EventType.CHANGE_LEVEL_3:
                newGame: GameInitialization = GameInitialization(3)

                return StateTransition(GameState.InitializeNewGame, newGame)
            
            if event == EventType.CHANGE_LEVEL_4:
                newGame: GameInitialization = GameInitialization(4)

                return StateTransition(GameState.InitializeNewGame, newGame)
            
            if event == EventType.CHANGE_LEVEL_5:
                newGame: GameInitialization = GameInitialization(5)

                return StateTransition(GameState.InitializeNewGame, newGame)
            
            if event == EventType.CHANGE_LEVEL_6:
                newGame: GameInitialization = GameInitialization(6)

                return StateTransition(GameState.InitializeNewGame, newGame)
            
            if event == EventType.NONE:
                break
            
        return None
    
    def _run_initial(self) -> StateTransition:

        nextState: StateTransition = StateTransition(GameState.Initial)

        while True:
            # events
            transition = self._process_ui_events()

            if transition != None:
                nextState = transition
                break

            # rendering
            self._renderer.compose([self._background])

            self._renderer.tick()

        return nextState

    def _run_game(self, state: GameState, game: Gameboard) -> StateTransition:

        nextState: StateTransition = StateTransition(GameState.GameOver)

        while True:
            # events
            transition = self._process_ui_events(game)

            if transition != None:
                nextState = transition
                break

            # rendering
            rendered_objects: list[RenderedObject] = []

            rendered_objects.append(self._background)

            # game pieces
            for boardItem in game.get_rendering_items():
                rendered_objects.append(boardItem)

            # status bar items
            radarStatus = StatusItem(-5)
            radarStatus.set_text(f"Radar contacts: {game.get_radar_contacts()} / {game.get_total_planes()}")

            rendered_objects.append(radarStatus)

            if state == GameState.GameOver:
                gameOverStatus = StatusItem(5)
                gameOverStatus.set_text(f"GAME OVER! Press Alt+N to start new game with same level or Alt+1 - Alt+6 to change level")

                rendered_objects.append(gameOverStatus)

            self._renderer.compose(rendered_objects)

            # check for game end
            if state != GameState.GameOver:
                game_result = game.is_finished()

                if game_result != None:
                    if game_result:
                        self._renderer.set_won_state()
                    else:
                        self._renderer.set_lost_state()

                    break
            
            self._renderer.tick()

        return nextState

    def run(self, initialState: GameState = GameState.Initial, gameInitialization: GameInitialization = None) -> bool:

        game: Gameboard = None
        state = initialState

        while state != GameState.Exit:

            transition: StateTransition = None

            if state == GameState.Initial:
                transition = self._run_initial()
            elif state == GameState.InitializeNewGame:
                nextState = GameState.SingleGame

                if gameInitialization == None:
                    # initialize new simple game board
                    game = Gameboard(1)
                    game.create()
                else:
                    game = Gameboard(gameInitialization.level)
                    game.create()

                    if not gameInitialization.singleGame:
                        nextState = GameState.ChallengeGame

                self._background.position_board_on_world(game)

                transition = StateTransition(nextState, game)
            elif state == GameState.SingleGame or state == GameState.ChallengeGame or state == GameState.GameOver:
                transition = self._run_game(state, game)

            if transition != None:
                state = transition.next

                if state == GameState.SingleGame or state == GameState.ChallengeGame:
                    game = transition.data
                    self._renderer.set_game_state()
                elif state == GameState.InitializeNewGame:
                    gameInitialization = transition.data
                elif state == GameState.Initial:
                    self._renderer.set_game_state()
            
