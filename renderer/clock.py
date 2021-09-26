from rgbmatrix.graphics import DrawText
from renderer.renderer import Renderer
from utils import align_text_center, load_font
from data.color import Color


class ClockRenderer(Renderer):
    """
    Render date and time

    Arguments:
        matrix (rgbmatrix.RGBMatrix):               RGBMatrix instance
        canvas (rgbmatrix.Canvas):                  Canvas associated with matrix
        data (data.Data):                           Data instance

    Attributes:
        date_color (rgbmatrix.graphics.Color):      Color for date text
        time_color (rgbmatrix.graphics.Color):      Color for time text
        fonts (dict):                               Fonts dictionary
        date_font (rgbmatrix.graphics.Font):        Font for date text
        time_font (rgbmatrix.graphics.Font):        Font for time text
        coords (dict):                              Coordinates dict
        date_x (int):                               Date text's x-coord
        date_y (int):                               Date text's y-coord
        time_x (int):                               Time text's x-coord
        time_y (int):                               Time text's y-coord
    """
    def __init__(self, matrix, canvas, data):
        super().__init__(matrix, canvas)
        self.data = data

        # Load data
        self.date = self.data.date
        self.time = self.data.time

        # Load colors
        self.date_color = Color.WHITE
        self.time_color = Color.WHITE

        # Load fonts
        self.fonts = self.data.config.layout['fonts']
        self.date_font = load_font(self.fonts['4x6'])
        self.time_font = load_font(self.fonts['cherry'])

        # Load coords
        self.coords = self.data.config.layout['coords']

        self.date_x = align_text_center(string=self.date,
                                        canvas_width=self.canvas.width,
                                        font_width=self.date_font.baseline - 1)[0] + 1
        self.date_y = self.coords['date']['y']

        self.time_x = align_text_center(string=self.time,
                                        canvas_width=self.canvas.width,
                                        font_width=self.time_font.baseline - 2)[0]
        self.time_y = self.coords['time']['y']

    def render(self):
        self.canvas.Clear()
        self.render_date()
        self.render_time()
        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def render_date(self):
        DrawText(self.canvas, self.date_font, self.date_x, self.date_y, self.date_color, self.date)

    def render_time(self):
        DrawText(self.canvas, self.time_font, self.time_x, self.time_y, self.time_color, self.time)
