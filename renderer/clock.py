import time

from renderer.renderer import Renderer
from util.utils import align_text


class ClockRenderer(Renderer):
    """
    Render date and time

    Arguments:
        data (api.Data):        Data instance

    Attributes:
        coords (dict):          Coordinates dictionary
    """

    def __init__(self, matrix, canvas, draw, config, data):
        super().__init__(matrix, canvas, draw, config)
        self.data = data
        self.coords = self.config.layout.coords['clock']

    def render(self):
        self.clear()
        self.render_date()
        self.render_time()
        self.matrix.SetImage(self.canvas)
        time.sleep(self.config.rotation_rate)

    def render_date(self):
        x = align_text(self.secondary_font.getsize(self.data.date),
                       self.matrix.width,
                       self.matrix.height)[0]
        y = self.coords['date']['y']
        self.draw.text((x, y), self.data.date, self.text_color, self.secondary_font)

    def render_time(self):
        x = align_text(self.config.layout.time_font.getsize(self.data.time),
                       self.matrix.width,
                       self.matrix.height)[0]
        y = self.coords['time']['y']
        self.draw.text((x, y), self.data.time, self.text_color, self.config.layout.time_font)
