from rgbmatrix import graphics
import utils as u

LED_STOCK_TICKER = "LED Stock Ticker"
VERSION = "v0.0.1"
LOADING = "LOADING"


# TODO: Create live Loading bar
class Loading:
    def __init__(self, matrix, config):
        self.matrix = matrix
        self.canvas = matrix.CreateFrameCanvas()

        # Load coords
        self.coords = config.layout["coords"]["loading"]

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

    def render(self):
        self.canvas.Clear()

        title_x = u.align_center(LED_STOCK_TICKER, (self.canvas.width/2), self.FONT_TOM_THUMB["width"])
        title_y = self.coords["title"]["y"]
        graphics.DrawText(self.canvas, self.primary_font, title_x, title_y, self.title_color, LED_STOCK_TICKER)

        loading_x = u.align_center(LOADING, (self.canvas.width/2), self.FONT_4X6["width"])
        loading_y = self.coords["text"]["y"]
        graphics.DrawText(self.canvas, self.secondary_font, loading_x, loading_y, self.loading_color, LOADING)

        version_x = u.align_right(VERSION, self.canvas.width, self.FONT_4X6["width"])
        version_y = self.coords["version"]["y"]
        graphics.DrawText(self.canvas, self.secondary_font, version_x, version_y, self.version_color, VERSION)

        self.canvas = self.matrix.SwapOnVSync(self.canvas)
