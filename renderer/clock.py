from rgbmatrix import graphics
import utils as u
import time

DATE_FORMAT = "%a, %B %d"  # eg. Sun, June 5
TWELVE_HOURS_DATE_FORMAT = "%I:%M %p"  # eg. 11:38 PM
TWENTY_FOUR_HOURS_DATE_FORMAT = "%H:%M"  # eg. 23:38


class ClockRenderer:
    def __init__(self, matrix, canvas, data):
        self.matrix = matrix
        self.canvas = canvas

        # Load data
        self.time_format = data.config.time_format
        self.date = self.get_date()
        self.time = self.get_time()

        # Load coords
        self.coords = data.config.layout["coords"]

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

    def render(self):
        date_x = u.align_center(self.date, (self.canvas.width/2), self.FONT_4X6["width"])
        date_y = self.coords["date"]["y"]

        time_x = u.align_center(self.time, (self.canvas.width/2), self.FONT_CHERRY["width"])
        time_y = self.coords["time"]["y"]

        self.canvas.Clear()
        graphics.DrawText(self.canvas, self.date_font, date_x + 1, date_y, self.date_color, self.date)
        graphics.DrawText(self.canvas, self.time_font, time_x, time_y, self.time_color, self.time)
        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    # Get current time
    def get_time(self):
        if self.time_format == "24h":
            return time.strftime(TWENTY_FOUR_HOURS_DATE_FORMAT)
        else:
            return time.strftime(TWELVE_HOURS_DATE_FORMAT)

    # Get current date
    def get_date(self):
        return time.strftime(DATE_FORMAT)

    # Refresh date and time
    def refresh(self):
        self.date = self.get_date()
        self.time = self.get_time()
