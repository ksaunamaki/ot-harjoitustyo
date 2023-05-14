import pygame
from primitives.interfaces import EventsCore
from primitives.events import EventData, EventType
from primitives.position import Position


class PygameEvents(EventsCore):
    """Implements event translation from Pygame events into internal EventData objects. 
    """
    def _get_kb(self, event: pygame.event.Event):
        modifiers = pygame.key.get_mods()
        is_alt = modifiers & pygame.KMOD_ALT
        is_numlock = modifiers & pygame.KMOD_NUM
        is_upcase = (modifiers & pygame.KMOD_CAPS) or\
                    (modifiers & pygame.KMOD_LSHIFT) or\
                    (modifiers & pygame.KMOD_RSHIFT)
        is_enter = event.unicode == '\r'

        if is_numlock:
            # Clear out numlock is set as Linux VMs could
            # reports this bogus status for modifiers
            modifiers &= ~pygame.KMOD_NUM

        if event.key == pygame.K_s and is_alt:
            return EventData(EventType.NEW_SINGLE_GAME)
        if event.key == pygame.K_c and is_alt:
            return EventData(EventType. NEW_CHALLENGE_GAME)
        if event.key == pygame.K_n and is_alt:
            return EventData(EventType.NEW_GAME)
        if event.key == pygame.K_1 and is_alt:
            return EventData(EventType.CHANGE_LEVEL_1)
        if event.key == pygame.K_2 and is_alt:
            return EventData(EventType.CHANGE_LEVEL_2)
        if event.key == pygame.K_3 and is_alt:
            return EventData(EventType.CHANGE_LEVEL_3)
        if event.key == pygame.K_4 and is_alt:
            return EventData(EventType.CHANGE_LEVEL_4)
        if event.key == pygame.K_5 and is_alt:
            return EventData(EventType.CHANGE_LEVEL_5)
        if event.key == pygame.K_6 and is_alt:
            return EventData(EventType.CHANGE_LEVEL_6)

        if not is_enter or is_upcase:
            return EventData(EventType.ALPHANUMERIC_KEY, None, event.unicode)

        return None

    def get(self) -> EventData:
        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            return EventData(EventType.EXIT)

        if event.type == pygame.MOUSEBUTTONDOWN:
            position = Position(event.dict["pos"][0],event.dict["pos"][1])
            button = event.dict["button"]

            if button == 1:
                return EventData(EventType.LEFT_CLICK, position)

            if button == 3:
                return EventData(EventType.RIGHT_CLICK, position)

        elif event.type == pygame.KEYDOWN:
            result = self._get_kb(event)

            if result is not None:
                return result

        return super().get()
