import pygame
from primitives.interfaces import EventsCore, EventType
from primitives.position import Position


class PygameEvents(EventsCore):
    def get(self) -> tuple[EventType, Position]:
        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            return (EventType.EXIT, None)

        if event.type == pygame.MOUSEBUTTONDOWN:
            position = Position(event.dict["pos"][0],event.dict["pos"][1])
            button = event.dict["button"]

            if button == 1:
                return (EventType.LEFT_CLICK, position)

            if button == 3:
                return (EventType.RIGHT_CLICK, position)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n and pygame.key.get_mods() & pygame.KMOD_ALT:
                return (EventType.NEW_GAME, None)
            if event.key == pygame.K_1 and pygame.key.get_mods() & pygame.KMOD_ALT:
                return (EventType.CHANGE_LEVEL_1, None)
            if event.key == pygame.K_2 and pygame.key.get_mods() & pygame.KMOD_ALT:
                return (EventType.CHANGE_LEVEL_2, None)
            if event.key == pygame.K_3 and pygame.key.get_mods() & pygame.KMOD_ALT:
                return (EventType.CHANGE_LEVEL_3, None)
            if event.key == pygame.K_4 and pygame.key.get_mods() & pygame.KMOD_ALT:
                return (EventType.CHANGE_LEVEL_4, None)
            if event.key == pygame.K_5 and pygame.key.get_mods() & pygame.KMOD_ALT:
                return (EventType.CHANGE_LEVEL_5, None)
            if event.key == pygame.K_6 and pygame.key.get_mods() & pygame.KMOD_ALT:
                return (EventType.CHANGE_LEVEL_6, None)

        return super().get()
