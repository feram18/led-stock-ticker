from renderer.renderer import Renderer
from renderer.stock import StockRenderer
from renderer.crypto import CryptoRenderer
from renderer.clock import ClockRenderer
from renderer.error import ErrorRenderer
from data.status import Status


class MainRenderer(Renderer):
    """
    Handle the rendering of different boards/screens (Clock, Stocks, Cryptos)

    Arguments:
        matrix (rgbmatrix.RGBMatrix):       RGBMatrix instance
        canvas (rgbmatrix.Canvas):          Canvas associated with matrix
        data (data.Data):                   Data instance

    Attributes:
        status (data.Status):               Update status
    """

    def __init__(self, matrix, canvas, data):
        super().__init__(matrix, canvas)
        self.data = data
        self.status = self.data.status

    def render(self):
        while self.status is Status.SUCCESS:
            try:
                self.render_clock()
                self.render_stocks()
                self.render_cryptos()

                if self.data.should_update():
                    self.status = self.data.update()

                self.data.update_clock()

            except KeyboardInterrupt as e:
                raise SystemExit(' Exiting...') from e

        self.render_error()

    def render_clock(self):
        ClockRenderer(self.matrix, self.canvas, self.data).render()

    def render_stocks(self):
        StockRenderer(self.matrix, self.canvas, self.data).render()

    def render_cryptos(self):
        CryptoRenderer(self.matrix, self.canvas, self.data).render()

    def render_error(self):
        ErrorRenderer(self.matrix, self.canvas, self.data).render()
