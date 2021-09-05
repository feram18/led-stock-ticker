import time
from constants import ROTATION_RATE
from renderer.ticker import TickerRenderer
from renderer.clock import ClockRenderer
from renderer.error import ErrorRenderer
from data.status import Status


class MainRenderer:
    """
    Handle the rendering of different boards/screens (Clock, Ticker)

    Arguments:
        matrix (rgbmatrix.RGBMatrix):       RGBMatrix instance
        data (data.Data):                   Data instance

    Attributes:
        canvas (rgbmatrix.Canvas):          Canvas associated with matrix

    """
    def __init__(self, matrix, data):
        self.matrix = matrix
        self.data = data

        self.canvas = matrix.CreateFrameCanvas()

    def render(self):
        while self.data.status != Status.FAIL:
            try:
                clock_renderer = ClockRenderer(self.matrix, self.canvas, self.data)
                clock_renderer.render()

                time.sleep(ROTATION_RATE)

                TickerRenderer(self.matrix, self.canvas, self.data).render()
                self.data.update()  # Update data for next run
            except KeyboardInterrupt:
                raise SystemExit(' Exiting...')

        if self.data.status != Status.SUCCESS:
            self.render_error()

    def render_error(self):
        ErrorRenderer(self.matrix, self.canvas, self.data.config, self.data.status).render()
