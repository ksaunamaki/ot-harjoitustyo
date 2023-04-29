import pygame
from primitives.interfaces import Renderer, RenderedObject, Asset
from primitives.position import Position
from primitives.border import Border
from primitives.color import Color
from primitives.size import Size
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

    def __init__(self,
                 window_title: str = None):
        super().__init__()

        pygame.init()

        if window_title is not None:
            pygame.display.set_caption()

        icon = AssetService.get_asset("icon")

        if icon is not None and icon.path is not None:
            pygame.display.set_icon(pygame.image.load(icon.path))

        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(
            (Renderer.WINDOW_WIDTH, Renderer.WINDOW_HEIGHT))
        self._status_font = pygame.font.Font(
            pygame.font.get_default_font(), 14)

        self._current_status_color = self._status_colors["game"]

        self._last_cursor_is_hand = False

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

    def _render_asset(self, asset: Asset, pos: Position) -> pygame.Rect:
        if asset.key not in self._loaded_images:
            self._loaded_images[asset.key] = pygame.image.load(asset.path)

        return self._screen.blit(self._loaded_images[asset.key], (pos.x, pos.y))

    def _render_text(self, text_object: TextObject, pos: Position) -> pygame.Rect:
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

        return self._screen.blit(rendered_text, (text_x, text_y))

    def _render_line(self, line: tuple[Position, Position, tuple[int, int, int]]):
        pygame.draw.line(self._screen,
                            pygame.Color(220, 220, 220),
                            (line[0].x, line[0].y),
                                (line[1].x, line[1].y))

    def _render_border(self, position: Position,
                       size: Size, border: Border):

        points = [(position.x, position.y),
                   (position.x + size.width, position.y),
                   (position.x + size.width, position.y + size.height),
                   (position.x, position.y + size.height)]

        pygame.draw.lines(self._screen,
                          (border.color.rgb_r,
                           border.color.rgb_g,
                           border.color.rgb_b),
                           True,
                           points,
                           border.thickness)

    def _render_background(self, position: Position,
                           size: Size, color: Color,
                           border: Border) -> pygame.Rect:

        rect = None

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
            rect = self._screen.blit(alpha_surface, (position.x, position.y))
        else:
            rect = pygame.draw.rect(self._screen,
                            pygame.Color(color.rgb_r,
                                color.rgb_g,
                                color.rgb_b),
                            pygame.Rect(position.x, position.y, size.width, size.height))

        if border is not None:
            self._render_border(position, size, border)

        return rect

    def _is_mouse_over_rendered(self,
                                obj_rect: pygame.Rect,
                                mouse_pos: tuple[int,int]) -> bool:
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]

        obj_x = obj_rect[0]
        obj_y = obj_rect[1]
        obj_width = obj_rect[2]
        obj_height = obj_rect[3]

        if mouse_x < obj_x or\
            mouse_x > obj_x + obj_width or\
            mouse_y < obj_y or\
            mouse_y > obj_y + obj_height:
            return False

        return True

    def _render_item(self,
                     obj: RenderedObject,
                     mouse_pos: tuple[int,int]) -> bool:
        background_size = obj.get_background_size()
        image_asset = obj.get_asset()
        text = obj.get_text()
        line = obj.get_line()
        rendered_rect = None

        pos = self.calculate_child_position(obj.get_position())

        if background_size is not None:
            rendered_rect = self._render_background(pos, background_size,
                                    obj.get_background_color(),
                                    obj.get_border())

        if image_asset is not None and image_asset.path is not None:
            rendered_asset_rect = self._render_asset(image_asset, pos)
            if rendered_rect is None:
                rendered_rect = rendered_asset_rect

        if text is not None:
            rendered_text_rect = self._render_text(text, pos)
            if rendered_rect is None:
                rendered_rect = rendered_text_rect

        if line is not None:
            self._render_line(line)

        return self._is_mouse_over_rendered(rendered_rect, mouse_pos)\
            if mouse_pos is not None and rendered_rect is not None else None

    def compose(self, objects: list[RenderedObject]):
        # main game area
        self._screen.fill(self._current_status_color)

        objects.sort(key=lambda rendered_object: rendered_object.get_z_order())

        # get cursor position
        cursor_pos = pygame.mouse.get_pos() if pygame.mouse.get_focused() else None
        over_object: RenderedObject = None

        # all objects
        for obj in objects:
            if self._render_item(obj, cursor_pos):
                over_object = obj

        if over_object is not None:
            if over_object.show_hand_cursor():
                if not self._last_cursor_is_hand:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    self._last_cursor_is_hand = True
            else:
                if self._last_cursor_is_hand:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    self._last_cursor_is_hand = False
        else:
            if self._last_cursor_is_hand:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                self._last_cursor_is_hand = False

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
