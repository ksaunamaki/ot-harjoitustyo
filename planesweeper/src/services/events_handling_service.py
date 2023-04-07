from primitives.interfaces import EventsCore, EventType
from primitives.position import Position
from primitives.game_state import GameState
from primitives.game_initialization import GameInitialization
from primitives.state_transition import StateTransition
from entities.board import Gameboard


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

    def _process_new_game_event(self, existing_game: Gameboard,
                                level: int = 1, single_game_mode = True) -> StateTransition:
        new_game: GameInitialization = None

        if existing_game is not None:
            if single_game_mode:
                new_game = GameInitialization(existing_game.get_level(), single_game_mode)
            else:
                # New challenge game from beginning
                new_game = GameInitialization(1, single_game_mode)
        else:
            new_game = GameInitialization(level, single_game_mode)

        return StateTransition(GameState.INITIALIZE_NEW_GAME, new_game)

    def _process_new_game_events(self, event: EventType,
                                  existing_game: Gameboard) -> StateTransition:

        if event == EventType.NEW_GAME:
            next_state = self._process_new_game_event(existing_game)

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


    def process_events(self, game: Gameboard) -> StateTransition:
        next_state: StateTransition = None

        while True:
            event, pos = self._events.get()

            if event == EventType.NONE:
                break # no more events

            if event == EventType.EXIT:
                next_state = StateTransition(GameState.EXIT)

            if event in (EventType.LEFT_CLICK, EventType.RIGHT_CLICK):
                next_state = self._process_mouse_left_click_event(pos, game)

            if event == EventType.RIGHT_CLICK:
                next_state = self._process_mouse_right_click_event(pos, game)

            if event in (EventType.NEW_GAME,
                         EventType.CHANGE_LEVEL_1,
                         EventType.CHANGE_LEVEL_2,
                         EventType.CHANGE_LEVEL_3,
                         EventType.CHANGE_LEVEL_4,
                         EventType.CHANGE_LEVEL_5,
                         EventType.CHANGE_LEVEL_6):
                next_state = self._process_new_game_events(event, game)

            if next_state is not None:
                break

        return next_state
    