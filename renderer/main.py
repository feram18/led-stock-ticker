from data.status import Status
from renderer.clock import ClockRenderer
from renderer.crypto import CryptoRenderer
from renderer.error import ErrorRenderer
from renderer.forex import ForexRenderer
from renderer.renderer import Renderer
from renderer.stock import StockRenderer


class MainRenderer(Renderer):
    """
    Handle the rendering of different boards/screens (Clock, Stocks, Cryptos, Forex)

    Arguments:
        data (api.Data):                        Data instance

    Attributes:
        status (data.Status):                   Update status
        clock (renderer.ClockRenderer):         Clock renderer instance
        stocks (renderer.StockRenderer):        Stocks renderer instance
        crypto (renderer.CryptoRenderer):       Crypto renderer instance
        forex (renderer.ForexRenderer):         Forex renderer instance
        error (renderer.ErrorRenderer):         Error renderer instance
    """

    def __init__(self, matrix, canvas, draw, config, data):
        super().__init__(matrix, canvas, draw, config)
        self.data = data
        self.status = self.data.status
        self.clock = ClockRenderer(self.matrix, self.canvas, self.draw, self.config, self.data)
        self.stocks = StockRenderer(self.matrix, self.canvas, self.draw, self.config, self.data)
        self.crypto = CryptoRenderer(self.matrix, self.canvas, self.draw, self.config, self.data)
        self.forex = ForexRenderer(self.matrix, self.canvas, self.draw, self.config, self.data)
        self.error = ErrorRenderer(self.matrix, self.canvas, self.draw, self.config, self.data)
        self.render()

    def render(self):
        while self.status is Status.SUCCESS:
            try:
                self.clock.render()
                self.stocks.render()
                self.crypto.render()
                self.forex.render()
                if self.data.should_update():
                    self.status = self.data.update()
                self.data.update_clock()
            except KeyboardInterrupt as e:
                raise SystemExit(' Exiting...') from e
        self.error.render()
