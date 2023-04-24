import unittest
from services.events_handling_service import InputBuffer, EventsHandlingService


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
