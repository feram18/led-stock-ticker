import time
from renderer.renderer import Renderer
from renderer.stock import StockRenderer
from renderer.crypto import CryptoRenderer
from renderer.clock import ClockRenderer
from renderer.error import ErrorRenderer
from constants import ROTATION_RATE
from data.status import Status


class MainRenderer(Renderer):
    """
    Handle the rendering of different boards/screens (Clock, Stocks, Cryptos)

    Arguments:
        matrix (rgbmatrix.RGBMatrix):       RGBMatrix instance
        data (data.Data):                   Data instance

    Attributes:
        canvas (rgbmatrix.Canvas):          Canvas associated with matrix

    """
    def __init__(self, matrix, canvas, data):
        super().__init__(matrix, canvas)
        self.data = data

    def render(self):
        while self.data.status != Status.FAIL:
            try:
                clock_renderer = ClockRenderer(self.matrix, self.canvas, self.data)
                clock_renderer.render()

                time.sleep(ROTATION_RATE)

                StockRenderer(self.matrix, self.canvas, self.data).render()
                CryptoRenderer(self.matrix, self.canvas, self.data).render()
                self.data.update()  # Update data for next run
            except KeyboardInterrupt as e:
                raise SystemExit(' Exiting...') from e

        if self.data.status != Status.SUCCESS:
            self.render_error()

    def render_error(self):
        ErrorRenderer(self.matrix, self.canvas, self.data.config, self.data.status).render()
