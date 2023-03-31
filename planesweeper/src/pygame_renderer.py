import pygame
from primitives.interfaces import Renderer, RenderedObject
from primitives.asset import Asset
from services.AssetService import AssetService

class PygameRenderer(Renderer):
    _loaded_images = {}
    _status_font: pygame.font.Font = None
    _statusColors = {
        "game": pygame.Color(0, 0, 0),
        "won": pygame.Color(0, 220, 0),
        "lost": pygame.Color(220, 0, 0)
    }

    def __init__(self):
        super().__init__()

        pygame.init()
        pygame.display.set_caption(super().WINDOW_TITLE)
        
        icon = AssetService.get_asset("icon")

        if icon != None and icon.path != None:
            pygame.display.set_icon(pygame.image.load(icon.path))

        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode((Renderer.WINDOW_WIDTH, Renderer.WINDOW_HEIGHT))
        self._status_font = pygame.font.Font(pygame.font.get_default_font(), 14)

        self._currentStatusColor = self._statusColors["game"]

    def _render_item(self, obj: RenderedObject):
        pos = obj.get_position()

        is_negative_xpos = False
        is_negative_ypos = False
        
        if pos[0] < 0:
            # calculate from end of window
            pos = (Renderer.WINDOW_WIDTH + pos[0], pos[1])
            is_negative_xpos = True

        if pos[1] < 0:
            # calculate from bottom of window
            pos = (pos[0], Renderer.WINDOW_HEIGHT + pos[1])
            is_negative_ypos = True

        asset = obj.get_asset()

        if asset != None and asset.path != None:
            if asset.key not in self._loaded_images:
                self._loaded_images[asset.key] = pygame.image.load(asset.path)

            self._screen.blit(self._loaded_images[asset.key], obj.get_position())

        text = obj.get_text()

        if text != None:
            text = self._status_font.render(text, True, pygame.Color(255,255,255))
            text_x = pos[0]
            text_y = pos[1]

            if is_negative_xpos:
                # move text's x position back width's worth
                text_x = pos[0] - text.get_width()

            if is_negative_ypos:
                # move text's y position back height's worth
                text_y = pos[1] - text.get_height()
            
            self._screen.blit(text, (text_x, text_y))

        line = obj.get_line()

        if line != None:
            pygame.draw.line(self._screen, pygame.Color(220, 220, 220), (line[0][0], line[0][1]),(line[1][0], line[1][1]))

    def compose(self, objects: list[RenderedObject]):
        # main game area
        self._screen.fill(self._currentStatusColor)

        # all objects
        for obj in objects:
            self._render_item(obj)

        pygame.display.flip()

    def tick(self):
        self._clock.tick(self._fps)

    def set_game_state(self):
        self._currentStatusColor = self._statusColors["game"]

    def set_won_state(self):
        self._currentStatusColor = self._statusColors["won"]

    def set_lost_state(self):
        self._currentStatusColor = self._statusColors["lost"]