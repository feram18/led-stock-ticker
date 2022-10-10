import time

from data.crypto import Crypto
from renderer.ticker import TickerRenderer


class CryptoRenderer(TickerRenderer):
    """
    Renderer for Crypto objects

    Attributes:
        cryptos (list):         List of Crypto objects
    """

    def __init__(self, matrix, canvas, draw, config, data):
        super().__init__(matrix, canvas, draw, config, data)
        self.cryptos: list = self.data.cryptos

    def render(self):
        for crypto in self.cryptos:
            self.populate_data(crypto)
            self.clear()
            self.render_name()
            self.render_symbol()
            self.render_price()
            self.render_percentage_change()
            self.render_chart()
            self.matrix.SetImage(self.canvas)
            time.sleep(self.config.rotation_rate)

    def populate_data(self, crypto: Crypto):
        """
        Populate attributes from Crypto instance's attributes.
        :param crypto: (data.Crypto) Crypto instance
        """
        super().populate_data(crypto)
        self.symbol = self.symbol.replace('-USD', '')  # Remove currency exchange

    def render_symbol(self):
        x = self.coords['crypto']['symbol']['x']
        y = self.coords['crypto']['symbol']['y']
        self.draw.text((x, y), self.symbol, self.text_color, self.large_font)
