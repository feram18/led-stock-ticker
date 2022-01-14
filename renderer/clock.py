import time
from rgbmatrix.graphics import DrawText
from renderer.renderer import Renderer
from utils import align_text, Position


class ClockRenderer(Renderer):
    """
    Render date and time

    Arguments:
        data (api.Data):        Data instance

    Attributes:
        date (str):             Current date string
        time (str):             Current time string
    """

    def __init__(self, matrix, canvas, config, data):
        super().__init__(matrix, canvas, config)
        self.data = data

        # Load data
        self.date = self.data.date
        self.time = self.data.time

    def render(self):
        self.canvas.Clear()

        self.render_date()
        self.render_time()

        time.sleep(self.config.rotation_rate)

        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def render_date(self):
        x = align_text(text=self.date,
                       x=Position.CENTER,
                       col_width=self.canvas.width,
                       font_width=self.secondary_font.baseline - 1) + 1
        y = self.config.layout.coords['date']['y']

        DrawText(self.canvas, self.secondary_font, x, y, self.text_color, self.date)

    def render_time(self):
        font = self.config.layout.time_font
        x = align_text(text=self.time,
                       x=Position.CENTER,
                       col_width=self.canvas.width,
                       font_width=font.baseline - 2)
        y = self.config.layout.coords['time']['y']
        DrawText(self.canvas, font, x, y, self.text_color, self.time)
