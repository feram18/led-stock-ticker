from constants import SCRIPT_NAME, SCRIPT_VERSION, LOADING_STR
from rgbmatrix import graphics
import utils as u


class Loading:
    """
    Render a splash screen while tickers' data is being fetched

    Properties:
        matrix        RGBMatrix instance
        config        Config instance
    """
    def __init__(self, matrix, config):
        self.matrix = matrix
        self.canvas = matrix.CreateFrameCanvas()

        # Load colors
        self.colors = config.colors["loading"]

        self.title_color = u.load_color(self.colors["title"])
        self.loading_color = u.load_color(self.colors["text"])
        self.version_color = u.load_color(self.colors["version"])

        # Load fonts
        self.fonts = config.layout["fonts"]

        self.FONT_TOM_THUMB = self.fonts["tom_thumb"]
        self.primary_font = u.load_font(self.FONT_TOM_THUMB["path"])

        self.FONT_4X6 = self.fonts["4x6"]
        self.secondary_font = u.load_font(self.FONT_4X6["path"])

        # Load coords
        self.coords = config.layout["coords"]["loading"]

        self.title_x = u.align_center(SCRIPT_NAME, (self.canvas.width / 2), self.FONT_TOM_THUMB["width"])
        self.title_y = self.coords["title"]["y"]

        self.loading_x = u.align_center(LOADING_STR, (self.canvas.width / 2), self.FONT_4X6["width"])
        self.loading_y = self.coords["text"]["y"]

        self.version_x = u.align_right(SCRIPT_VERSION, self.canvas.width, self.FONT_4X6["width"])
        self.version_y = self.coords["version"]["y"]

    def render(self):
        self.canvas.Clear()

        self.__render_title()
        self.__render_loading_text()
        self.__render_version()

        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def __render_title(self):
        return graphics.DrawText(self.canvas,
                                 self.primary_font,
                                 self.title_x,
                                 self.title_y,
                                 self.title_color,
                                 SCRIPT_NAME)

    def __render_loading_text(self):
        return graphics.DrawText(self.canvas,
                                 self.secondary_font,
                                 self.loading_x,
                                 self.loading_y,
                                 self.loading_color,
                                 LOADING_STR)

    def __render_version(self):
        return graphics.DrawText(self.canvas,
                                 self.secondary_font,
                                 self.version_x,
                                 self.version_y,
                                 self.version_color,
                                 SCRIPT_VERSION)
