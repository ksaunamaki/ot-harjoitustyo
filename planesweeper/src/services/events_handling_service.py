from primitives.interfaces import EventsCore
from primitives.event_type import EventType
from primitives.position import Position
from primitives.game_state import GameState
from primitives.game_mode import GameMode
from primitives.game_initialization import GameInitialization
from primitives.state_transition import StateTransition
from entities.board import Gameboard


class InputBuffer:
    def __init__(self):
        self._buffer = ""
        self._updated = False

    def write(self, data: str):
        self._buffer += data
        self._updated = True

    def read(self) -> str:
        self._updated = False
        buffer = self._buffer
        self._buffer = ""

        return buffer

    @property
    def is_updated(self) -> bool:
        updated = self._updated
        self._updated = False

        return updated

class EventsHandlingService:

    def __init__(self, events: EventsCore):
        self._events = events

    def _get_game_piece_position(self, event_pos: Position, game: Gameboard) -> Position:
        if game is None:
            return None

        return game.translate_event_position_to_piece_position(event_pos)

    def _process_mouse_left_click_event(self, pos: Position, game: Gameboard) -> StateTransition:
        next_state: StateTransition = None

        piece_position = self._get_game_piece_position(pos, game)

        if piece_position is not None:
            game.open_piece(piece_position)

        return next_state

    def _process_mouse_right_click_event(self, pos: Position, game: Gameboard) -> StateTransition:
        next_state: StateTransition = None

        piece_position = self._get_game_piece_position(pos, game)

        if piece_position is not None:
            game.mark_piece(piece_position)

        return next_state

    def _process_mouse_click_event(self,
                                   current_state: GameState,
                                   event: EventType,
                                   pos: Position,
                                   game: Gameboard) -> StateTransition:

        # While inputting, do not react to clicks
        if current_state == GameState.GET_INITIALS:
            return None

        if event == EventType.LEFT_CLICK:
            return self._process_mouse_left_click_event(pos, game)

        return self._process_mouse_right_click_event(pos, game)

    def _process_new_game_event(self,
                                existing_game: Gameboard,
                                level: int = 1,
                                mode: GameMode = GameMode.SINGLE_GAME) -> StateTransition:
        new_game: GameInitialization = None

        if existing_game is not None:
            if mode == GameMode.SINGLE_GAME:
                new_game = GameInitialization(existing_game.get_level(), mode)
            else:
                # New challenge game from beginning
                new_game = GameInitialization(1, mode)
        else:
            new_game = GameInitialization(level, mode)

        return StateTransition(GameState.INITIALIZE_NEW_GAME, new_game)

    def _process_new_game_events(self,
                                 event: EventType,
                                 game_initialization: GameInitialization,
                                 existing_game: Gameboard) -> StateTransition:

        if event == EventType.NEW_GAME:
            next_state = self._process_new_game_event(existing_game, 1, game_initialization.mode)

        if event == EventType.CHANGE_LEVEL_1:
            next_state = self._process_new_game_event(None, 1)

        if event == EventType.CHANGE_LEVEL_2:
            next_state = self._process_new_game_event(None, 2)

        if event == EventType.CHANGE_LEVEL_3:
            next_state = self._process_new_game_event(None, 3)

        if event == EventType.CHANGE_LEVEL_4:
            next_state = self._process_new_game_event(None, 4)

        if event == EventType.CHANGE_LEVEL_5:
            next_state = self._process_new_game_event(None, 5)

        if event == EventType.CHANGE_LEVEL_6:
            next_state = self._process_new_game_event(None, 6)

        return next_state

    def process_events(self,
                       current_state: GameState,
                       game_initialization: GameInitialization,
                       game: Gameboard,
                       input_buffer: InputBuffer = None) -> StateTransition:
        next_state: StateTransition = None

        while True:
            data = self._events.get()

            if data.event == EventType.NONE:
                break # no more events

            if data.event == EventType.EXIT:
                next_state = StateTransition(GameState.EXIT)

            if data.event in (EventType.LEFT_CLICK, EventType.RIGHT_CLICK):
                next_state = self._process_mouse_click_event(
                    current_state,
                    data.event,
                    data.position,
                    game)

            if data.event in (EventType.NEW_GAME,
                         EventType.CHANGE_LEVEL_1,
                         EventType.CHANGE_LEVEL_2,
                         EventType.CHANGE_LEVEL_3,
                         EventType.CHANGE_LEVEL_4,
                         EventType.CHANGE_LEVEL_5,
                         EventType.CHANGE_LEVEL_6):
                next_state = self._process_new_game_events(data.event, game_initialization, game)

            if data.event == EventType.ALPHANUMERIC_KEY and input_buffer is not None:
                input_buffer.write(data.data)

            if next_state is not None:
                break

        return next_state
    