import unittest
from primitives.interfaces import EventsCore, Renderer, EventData, EventType
from primitives.position import Position
from primitives.size import Size
from services.events_handling_service import InputBuffer, EventsHandlingService
from primitives.game import GameState
from entities.ui.button import Button

class EventsMock(EventsCore):
    keypresses = "ABCDEFGHIJKLMNOPQRSTUVWX"

    def __init__(self,
                 supply_mouseleft_events: bool = False,
                 supply_mouseright_events: bool = False,
                 click_pos: Position = None,
                 supply_keypresses: bool = False, 
                 count: int = 1):
        self.supply_mouseleft_events = supply_mouseleft_events
        self.supply_mouseright_events = supply_mouseright_events
        self.position = click_pos
        self.supply_keypresses = supply_keypresses
        self.count = count
        self.emitted = 0

    def get(self) -> EventData:
        data = EventData(EventType.NONE, None, None)

        if self.emitted < self.count:
            if self.supply_mouseleft_events:
                data = EventData(EventType.LEFT_CLICK, self.position, None)
            elif self.supply_mouseright_events:
                data = EventData(EventType.RIGHT_CLICK, self.position, None)
            elif self.supply_keypresses:
                data = EventData(EventType.ALPHANUMERIC_KEY, None, self.keypresses[self.emitted % len(self.keypresses)])
            
        self.emitted += 1
        
        return data

class TestEventsHandling(unittest.TestCase):
    def setUp(self):
        pass

    def test_input_buffer_updated_status_clears(self):
        buffer = InputBuffer()

        buffer.write("AAA")

        self.assertEqual(buffer.is_updated, True)
        self.assertEqual(buffer.is_updated, False)

    def test_input_buffer_reads_once(self):
        buffer = InputBuffer()

        buffer.write("AAA")
        data = buffer.read()

        self.assertEqual(data, "AAA")

        data = buffer.read()

        self.assertEqual(data, "")

    def test_button_click_detected(self):
        mock_events = EventsMock(True, False, Position(10,10))
        service = EventsHandlingService(mock_events)
        state = GameState.INITIAL
        event_data_on_click = EventData(EventType.NEW_SINGLE_GAME) # click should cause new game to be selected
        buttons = [Button("", 14, Position(0,0), None, Position(5,5), Size(100, 100), None, None, event_data_on_click, Renderer())]

        transition = service.process_events(state, None, None, buttons)

        self.assertIsNotNone(transition)
        self.assertEqual(transition.next, GameState.INITIALIZE_NEW_GAME)

    def test_button_outside_click_not_detected(self):
        mock_events = EventsMock(True, False, Position(2,2))
        service = EventsHandlingService(mock_events)
        state = GameState.INITIAL
        event_data_on_click = EventData(EventType.NEW_SINGLE_GAME) # click should cause new game to be selected
        buttons = [Button("", 14, Position(0,0), None, Position(5,5), Size(100, 100), None, None, event_data_on_click, Renderer())]

        transition = service.process_events(state, None, None, buttons)

        self.assertIsNone(transition)

    def test_kb_initial_input_works(self):
        keypresses_count = 5
        mock_events = EventsMock(False, False, None, True, keypresses_count)
        service = EventsHandlingService(mock_events)
        state = GameState.GET_INITIALS

        buffer = InputBuffer()
        
        transition = service.process_events(state, None, None, None, buffer)

        read = buffer.read()

        self.assertIsNone(transition)
        self.assertEqual(read, EventsMock.keypresses[:keypresses_count])
