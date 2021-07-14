from constants import DATE_FORMAT, TWELVE_HOURS_DATE_FORMAT, TWENTY_FOUR_HOURS_DATE_FORMAT
from rgbmatrix import graphics
import utils as u
import time


class ClockRenderer:
    """
    Render date and time

    Properties:
        matrix      RGBMatrix instance
        canvas      Canvas associated with matrix
        data        Data instance
    """
    def __init__(self, matrix, canvas, data):
        self.matrix = matrix
        self.canvas = canvas

        # Load data
        self.time_format = data.config.time_format
        self.date = self.get_date()
        self.time = self.get_time()

        # Load colors
        self.colors = data.config.colors["clock"]
        self.date_color = u.load_color(self.colors["date"])
        self.time_color = u.load_color(self.colors["time"])

        # Load fonts
        self.fonts = data.config.layout["fonts"]

        self.FONT_4X6 = self.fonts["4x6"]
        self.date_font = u.load_font(self.FONT_4X6["path"])

        self.FONT_CHERRY = self.fonts["cherry"]
        self.time_font = u.load_font(self.FONT_CHERRY["path"])

        # Load coords
        self.coords = data.config.layout["coords"]

        self.date_x = u.align_center(self.date, (self.canvas.width / 2), self.FONT_4X6["width"])
        self.date_y = self.coords["date"]["y"]

        self.time_x = u.align_center(self.time, (self.canvas.width / 2), self.FONT_CHERRY["width"])
        self.time_y = self.coords["time"]["y"]

    def render(self):
        self.canvas.Clear()

        self.__render_date()
        self.__render_time()

        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def __render_date(self):
        return graphics.DrawText(self.canvas, self.date_font, self.date_x + 1, self.date_y, self.date_color, self.date)

    def __render_time(self):
        return graphics.DrawText(self.canvas, self.time_font, self.time_x, self.time_y, self.time_color, self.time)

    def get_time(self) -> str:
        if self.time_format is "24h":
            return time.strftime(TWENTY_FOUR_HOURS_DATE_FORMAT)
        else:
            return time.strftime(TWELVE_HOURS_DATE_FORMAT)

    @staticmethod
    def get_date() -> str:
        return time.strftime(DATE_FORMAT)

    def refresh(self):
        self.date = self.get_date()
        self.time = self.get_time()
