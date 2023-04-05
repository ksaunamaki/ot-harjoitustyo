import pygame
from primitives.interfaces import Renderer, RenderedObject, Asset
from primitives.position import Position
from services.asset_service import AssetService


class PygameRenderer(Renderer):
    _loaded_images = {}
    _status_font: pygame.font.Font = None
    _status_colors = {
        "game": pygame.Color(0, 0, 0),
        "won": pygame.Color(0, 220, 0),
        "lost": pygame.Color(220, 0, 0)
    }

    def __init__(self):
        super().__init__()

        pygame.init()
        pygame.display.set_caption(super().WINDOW_TITLE)

        icon = AssetService.get_asset("icon")

        if icon is not None and icon.path is not None:
            pygame.display.set_icon(pygame.image.load(icon.path))

        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(
            (Renderer.WINDOW_WIDTH, Renderer.WINDOW_HEIGHT))
        self._status_font = pygame.font.Font(
            pygame.font.get_default_font(), 14)

        self._current_status_color = self._status_colors["game"]

    def _render_asset(self, asset: Asset, pos: Position):
        if asset is not None and asset.path is not None:
            if asset.key not in self._loaded_images:
                self._loaded_images[asset.key] = pygame.image.load(asset.path)

            self._screen.blit(self._loaded_images[asset.key], (pos.x, pos.y))

    def _render_text(self, text: str, pos: Position,
                     is_negative_xpos: bool, is_negative_ypos: bool):
        if text is not None:
            text = self._status_font.render(
                text, True, pygame.Color(255, 255, 255))
            text_x = pos.x
            text_y = pos.y

            if is_negative_xpos:
                # move text's x position back width's worth
                text_x = pos.x - text.get_width()

            if is_negative_ypos:
                # move text's y position back height's worth
                text_y = pos.y - text.get_height()

            self._screen.blit(text, (text_x, text_y))

    def _render_line(self, line: tuple[Position, Position, tuple[int, int, int]]):
        if line is not None:
            pygame.draw.line(self._screen,
                             pygame.Color(220, 220, 220),
                               (line[0].x, line[0].y),
                                 (line[1].x, line[1].y))

    def _render_item(self, obj: RenderedObject):
        pos = obj.get_position()

        is_negative_xpos = False
        is_negative_ypos = False

        if pos.x < 0:
            # calculate from end of window
            pos = Position(Renderer.WINDOW_WIDTH + pos.x, pos.y)
            is_negative_xpos = True

        if pos.y < 0:
            # calculate from bottom of window
            pos = Position(pos.x, Renderer.WINDOW_HEIGHT + pos.y)
            is_negative_ypos = True

        self._render_asset(obj.get_asset(), pos)
        self._render_text(obj.get_text(), pos, is_negative_xpos, is_negative_ypos)
        self._render_line(obj.get_line())

    def compose(self, objects: list[RenderedObject]):
        # main game area
        self._screen.fill(self._current_status_color)

        # all objects
        for obj in objects:
            self._render_item(obj)

        pygame.display.flip()

    def tick(self):
        self._clock.tick(self._fps)

    def set_game_state(self):
        self._current_status_color = self._status_colors["game"]

    def set_won_state(self):
        self._current_status_color = self._status_colors["won"]

    def set_lost_state(self):
        self._current_status_color = self._status_colors["lost"]
