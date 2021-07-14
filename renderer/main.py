from constants import REFRESH_DELAY
from .ticker import TickerRenderer
from .clock import ClockRenderer
import time
import sys


class MainRenderer:
    """
    Handle the rendering of different boards (Clock, Ticker)

    Properties:
        matrix      RGBMatrix instance
        data        Data instance
    """
    def __init__(self, matrix, data):
        self.matrix = matrix
        self.canvas = matrix.CreateFrameCanvas()
        self.data = data

    def render(self):
        while True:
            try:
                clock_renderer = ClockRenderer(self.matrix, self.canvas, self.data)
                clock_renderer.render()

                self.data.refresh_tickers()
                time.sleep(REFRESH_DELAY)

                TickerRenderer(self.matrix, self.canvas, self.data).render()

                # Refresh data for next run
                clock_renderer.refresh()
            except KeyboardInterrupt:
                sys.exit(0)
