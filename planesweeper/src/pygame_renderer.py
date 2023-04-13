import pygame
from primitives.interfaces import Renderer, RenderedObject, Asset
from primitives.position import Position
from primitives.size import Size
from primitives.color import Color
from primitives.text_object import TextObject
from services.asset_service import AssetService


class PygameRenderer(Renderer):
    _loaded_images = {}
    _fonts = {}
    _text_measurement_cache = {}
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

    def _calculate_positioning(self, pos: Position, container_size: Size = None) -> Position:
        actual_positioning = Position(pos.x, pos.y)

        container_width = container_size.width\
            if container_size is not None\
            else Renderer.WINDOW_WIDTH

        container_height = container_size.height\
            if container_size is not None\
            else Renderer.WINDOW_HEIGHT

        if pos.x < 0:
            # calculate from end of container
            actual_positioning.x = container_width + pos.x

        if pos.y < 0:
            # calculate from bottom of container
            actual_positioning.y = container_height + pos.y

        return actual_positioning

    def _get_font_for_text(self, font_size: int) -> pygame.font.Font:
        if font_size is None:
            # get default size'd font
            font_size = 11

        font = None

        if font_size not in self._fonts:
            font = pygame.font.Font(pygame.font.get_default_font(), font_size)
        else:
            font = self._fonts[font_size]

        return font

    def _get_rendered_text(self, text_object: TextObject) -> pygame.Surface:
        font = self._get_font_for_text(text_object.get_size())
        color = text_object.get_color()

        return font.render(text_object.get_text(),
                                    True,
                                    pygame.Color(color.rgb_r,
                                                 color.rgb_g,
                                                 color.rgb_b,
                                                 color.alpha * 255))

    def _render_asset(self, asset: Asset, pos: Position):
        if asset.key not in self._loaded_images:
            self._loaded_images[asset.key] = pygame.image.load(asset.path)

        self._screen.blit(self._loaded_images[asset.key], (pos.x, pos.y))

    def _render_text(self, text_object: TextObject, pos: Position):
        relative_pos = text_object.get_position()
        rendered_text = self._get_rendered_text(text_object)

        text_x = pos.x
        text_y = pos.y

        if relative_pos.x < 0:
            # move text's x position back width's worth + relarive offset
            text_x = pos.x - rendered_text.get_width() + relative_pos.x
        else:
            text_x = pos.x + relative_pos.x

        if relative_pos.y < 0:
            # move text's y position back height's worth + relarive offset
            text_y = pos.y - rendered_text.get_height() + relative_pos.y
        else:
            text_y = pos.y + relative_pos.y

        self._screen.blit(rendered_text, (text_x, text_y))

    def _render_line(self, line: tuple[Position, Position, tuple[int, int, int]]):
        pygame.draw.line(self._screen,
                            pygame.Color(220, 220, 220),
                            (line[0].x, line[0].y),
                                (line[1].x, line[1].y))

    def _render_background(self, position: Position,
                           size: Size, color: Color):
        if color is None:
            color = Color(255,255,255)

        if color.alpha < 255:
            # pygame.draw doesn't support alpha, must workaround
            alpha_surface = pygame.Surface((size.width, size.height), pygame.SRCALPHA)
            alpha_surface.fill(pygame.Color(
                                color.rgb_r,
                                color.rgb_g,
                                color.rgb_b,
                                int(color.alpha * 255)))
            self._screen.blit(alpha_surface, (position.x, position.y))
            return

        pygame.draw.rect(self._screen,
                         pygame.Color(color.rgb_r,
                            color.rgb_g,
                            color.rgb_b),
                        pygame.Rect(position.x, position.y, size.width, size.height))

    def _render_item(self, obj: RenderedObject):
        background_size = obj.get_background_size()
        image_asset = obj.get_asset()
        text = obj.get_text()
        line = obj.get_line()

        pos = self._calculate_positioning(obj.get_position())

        if background_size is not None:
            self._render_background(pos, background_size, obj.get_background_color())

        if image_asset is not None and image_asset.path is not None:
            self._render_asset(image_asset, pos)

        if text is not None:
            self._render_text(text, pos)

        if line is not None:
            self._render_line(line)

    def compose(self, objects: list[RenderedObject]):
        # main game area
        self._screen.fill(self._current_status_color)

        objects.sort(key=lambda rendered_object: rendered_object.get_z_order())

        # all objects
        for obj in objects:
            self._render_item(obj)

        pygame.display.flip()

    def tick(self):
        self._clock.tick(self._fps)

    def get_fps(self) -> int:
        return self._fps

    def set_game_state(self):
        self._current_status_color = self._status_colors["game"]

    def set_won_state(self):
        self._current_status_color = self._status_colors["won"]

    def set_lost_state(self):
        self._current_status_color = self._status_colors["lost"]

    def measure_text_dimensions(self, text_object: TextObject) -> Size:
        if text_object is None:
            return None

        text = text_object.get_text()
        text_size = text_object.get_size()
        cache_key = (text, text_size)
        measured_size: Size = None

        if cache_key not in self._text_measurement_cache:
            rendered_text = self._get_rendered_text(text_object)
            measured_size = Size(rendered_text.get_width(), rendered_text.get_height())
            self._text_measurement_cache[cache_key] = measured_size
        else:
            measured_size = self._text_measurement_cache[cache_key]

        return measured_size
