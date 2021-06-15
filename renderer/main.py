from clock import ClockRenderer
from stock import StockRenderer
import time
import sys

SHORT_DELAY = 5.0
ROTATION_DELAY = 15.0


class MainRenderer:
    def __init__(self, matrix, data):
        self.matrix = matrix
        self.canvas = matrix.CreateFrameCanvas()
        self.data = data

    def render(self):
        while True:
            try:
                clock_renderer = ClockRenderer(self.matrix, self.canvas, self.data)
                clock_renderer.render()

                self.data.refresh_symbols()
                time.sleep(SHORT_DELAY)

                StockRenderer(self.matrix, self.canvas, self.data).render()

                # Refresh data for next run
                clock_renderer.refresh()
            except KeyboardInterrupt:
                sys.exit(0)
