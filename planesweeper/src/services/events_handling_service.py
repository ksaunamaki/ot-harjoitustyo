from primitives.interfaces import EventsCore, EventData, Renderer
from primitives.events import EventType
from primitives.position import Position
from primitives.game import GameState, GameMode, GameInitialization
from primitives.state_transition import StateTransition
from entities.board import Gameboard
from entities.ui.button import Button


class InputBuffer:
    """Input buffer to use for holding keyboard input text before main loop can process
        it.
    """
    def __init__(self):
        self._buffer = ""
        self._updated = False

    def write(self, data: str):
        """Add new input text to the buffer.

        Args:
            data (str): Text to add.
        """
        self._buffer += data
        self._updated = True

    def read(self) -> str:
        """Gets the buffered text and clears the buffer.

        Returns:
            str: Currently buffered text.
        """
        self._updated = False
        buffer = self._buffer
        self._buffer = ""

        return buffer

    @property
    def is_updated(self) -> bool:
        """Signals if input buffer has been written to after last check or read.

        Returns:
            bool: True if new data is available since last check or read.
        """
        updated = self._updated
        self._updated = False

        return updated

class EventsHandlingResult:
    def __init__(self,
                 next_state: StateTransition,
                 new_event: EventData = None):
        self._next_state = next_state
        self._new_event = new_event

    @property
    def next_state(self) -> StateTransition:
        return self._next_state

    @property
    def new_event(self) -> EventData:
        return self._new_event

class EventsHandlingService:
    """Handles UI events (mouse and keyboard) translation into game state changes.
    """

    def __init__(self,
                 events: EventsCore = EventsCore(),
                 renderer: Renderer = Renderer()):
        """Initialize service.

        Args:
            events (EventsCore, optional): EventCore derived class implementation that
                supplies detected UI events for handling. Defaults to EventsCore().
            renderer (Renderer, optional): Renderer derived class implementation that
                can be used to calculate object positionings. Defaults to Renderer().
        """
        self._events: EventsCore = events
        self._renderer: Renderer = renderer

    def _get_game_piece_position(self, event_pos: Position, game: Gameboard) -> Position:
        if game is None:
            return None

        return game.translate_event_position_to_piece_position(event_pos)

    def _check_for_button_click(self,
                                mouse_pos: Position,
                                ui_buttons: list[Button]) -> EventsHandlingResult:

        for button in ui_buttons:
            obj_pos = self._renderer.calculate_child_position(button.get_position())
            obj_size = button.get_background_size()

            if mouse_pos.x < obj_pos.x or\
                mouse_pos.x > obj_pos.x + obj_size.width or\
                mouse_pos.y < obj_pos.y or\
                mouse_pos.y > obj_pos.y + obj_size.height:
                continue

            return EventsHandlingResult(None, button.get_click_event())

        return None

    def _process_mouse_left_click_event(self,
                                        pos: Position,
                                        game: Gameboard,
                                        ui_buttons: list[Button]) -> EventsHandlingResult:
        next_state: StateTransition = None

        # check for button presses first
        if ui_buttons is not None and len(ui_buttons) > 0:
            event_handling_result = self._check_for_button_click(pos, ui_buttons)
            if event_handling_result is not None:
                return event_handling_result

        piece_position = self._get_game_piece_position(pos, game)

        if piece_position is not None:
            game.open_piece(piece_position)

        return EventsHandlingResult(next_state)

    def _process_mouse_right_click_event(self,
                                         pos: Position,
                                         game: Gameboard) -> EventsHandlingResult:
        next_state: StateTransition = None

        piece_position = self._get_game_piece_position(pos, game)

        if piece_position is not None:
            game.mark_piece(piece_position)

        return EventsHandlingResult(next_state)

    def _process_mouse_click_event(self,
                                   current_state: GameState,
                                   event: EventType,
                                   pos: Position,
                                   game: Gameboard,
                                   ui_buttons: list[Button]) -> EventsHandlingResult:

        # While inputting, do not react to clicks
        if current_state == GameState.GET_INITIALS:
            return EventsHandlingResult(None)

        if event == EventType.LEFT_CLICK:
            return self._process_mouse_left_click_event(pos, game, ui_buttons)

        return self._process_mouse_right_click_event(pos, game)

    def _process_new_game_event(self,
                                existing_game: Gameboard,
                                level: int = 1,
                                mode: GameMode = GameMode.SINGLE_GAME) -> EventsHandlingResult:
        new_game: GameInitialization = None

        if existing_game is not None:
            if mode == GameMode.SINGLE_GAME:
                new_game = GameInitialization(existing_game.get_level(), mode)
            else:
                # New challenge game from beginning
                new_game = GameInitialization(1, mode)
        else:
            new_game = GameInitialization(level, mode)

        return EventsHandlingResult(StateTransition(GameState.INITIALIZE_NEW_GAME, new_game))

    def _process_new_game_events(self,
                                 current_state: GameState,
                                 event: EventType,
                                 game_initialization: GameInitialization,
                                 existing_game: Gameboard) -> EventsHandlingResult:

        next_state = None

        if event == EventType.NEW_GAME and current_state != GameState.INITIAL:
            next_state = self._process_new_game_event(existing_game, 1, game_initialization.mode)

        if event == EventType.NEW_CHALLENGE_GAME:
            next_state = self._process_new_game_event(None, 1, GameMode.CHALLENGE_GAME)

        if event in (EventType.NEW_SINGLE_GAME, EventType.CHANGE_LEVEL_1):
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

    def _process_event(self,
                       data: EventData,
                       current_state: GameState,
                       game_initialization: GameInitialization,
                       game: Gameboard,
                       ui_buttons: list[Button] = None,
                       input_buffer: InputBuffer = None) -> StateTransition:
        result: EventsHandlingResult = EventsHandlingResult(None)
        next_state = None

        while result is not None:
            if data.event == EventType.EXIT:
                next_state = StateTransition(GameState.EXIT)
                break

            if data.event in (EventType.LEFT_CLICK, EventType.RIGHT_CLICK):
                result = self._process_mouse_click_event(
                    current_state,
                    data.event,
                    data.position,
                    game,
                    ui_buttons)

            if data.event in (
                        EventType.NEW_SINGLE_GAME,
                        EventType.NEW_CHALLENGE_GAME,
                        EventType.NEW_GAME,
                        EventType.CHANGE_LEVEL_1,
                        EventType.CHANGE_LEVEL_2,
                        EventType.CHANGE_LEVEL_3,
                        EventType.CHANGE_LEVEL_4,
                        EventType.CHANGE_LEVEL_5,
                        EventType.CHANGE_LEVEL_6):
                result = self._process_new_game_events(
                    current_state,
                    data.event,
                    game_initialization,
                    game)

            if data.event == EventType.ALPHANUMERIC_KEY and input_buffer is not None:
                input_buffer.write(data.data)

            if result is None:
                break

            if result.next_state is not None:
                next_state = result.next_state
                break

            if result.new_event is not None:
                # reprocess
                data = result.new_event
            else:
                result = None

        return next_state

    def process_events(self,
                       current_state: GameState,
                       game_initialization: GameInitialization,
                       game: Gameboard,
                       ui_buttons: list[Button] = None,
                       input_buffer: InputBuffer = None) -> StateTransition:
        """Processes UI events that are supplied by the EventCore class.

        Args:
            current_state (GameState): Current main game loop state for program.
            game_initialization (GameInitialization): Currently running game's initialization
                information, if applicable to current state.
            game (Gameboard): Currently running game's gameboard, if applicable to current state.
            ui_buttons (list[Button], optional): Visible UI buttons that need to be
                tested for click events, if applicable to current state. Defaults to None.
            input_buffer (InputBuffer, optional): Keyboard input buffer active for reading
                input from user, if applicable to current state. Defaults to None.

        Returns:
            StateTransition: State transition required as response for UI events, or None.
        """
        next_state: StateTransition = None

        while True:
            data = self._events.get()

            if data.event == EventType.NONE:
                break # no more events

            next_state = self._process_event(
                                data,
                                current_state,
                                game_initialization,
                                game,
                                ui_buttons,
                                input_buffer)

            if next_state is not None:
                break

        return next_state
    