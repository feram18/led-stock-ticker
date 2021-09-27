import time
import utils
from renderer.ticker import TickerRenderer
from data.crypto import Crypto
from constants import TEXT_SCROLL_SPEED, TEXT_SCROLL_DELAY, ROTATION_RATE


class CryptoRenderer(TickerRenderer):
    """
    Renderer for Crypto objects

    Arguments:
        matrix (rgbmatrix.RGBMatrix):       RGBMatrix instance
        canvas (rgbmatrix.Canvas):          Canvas associated with matrix
        data (data.Data):                   Data instance

    Attributes:
        cryptos (list):                     List of Crypto objects
    """

    def __init__(self, matrix, canvas, data):
        super().__init__(matrix, canvas, data)
        self.symbol_x = 0
        self.cryptos = self.data.cryptos

    def render(self):
        for crypto in self.cryptos:
            self.populate_data(crypto)
            self.canvas.Clear()

            if utils.text_offscreen(self.name, self.canvas.width, self.primary_font.baseline - 1):
                time_started = time.time()
                first_run = True
                self.name_x = 1

                while not self.finished_scrolling:
                    self.canvas.Clear()

                    # Render elements
                    self.render_chart()
                    pos = self.render_name()
                    self.render_symbol()
                    self.render_price()
                    self.render_percentage_change()

                    if first_run:
                        time.sleep(TEXT_SCROLL_DELAY)
                        first_run = False

                    time.sleep(TEXT_SCROLL_SPEED)

                    self.name_x = utils.scroll_text(self.canvas.width, self.name_x, pos)

                    if time.time() - time_started >= ROTATION_RATE:
                        self.finished_scrolling = True
            else:
                self.name_x = utils.align_text_center(string=self.name,
                                                      canvas_width=self.canvas.width,
                                                      font_width=self.primary_font.baseline - 1)[0]

                # Render elements
                self.render_chart()
                self.render_name()
                self.render_symbol()
                self.render_price()
                self.render_percentage_change()

                time.sleep(ROTATION_RATE)

            self.finished_scrolling = False
            self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def populate_data(self, crypto: Crypto):
        """
        Populate attributes from Crypto instance's attributes.
        :param crypto: (data.Crypto) Crypto instance
        """
        super().populate_data(crypto)
        self.symbol = self.format_symbol(crypto.symbol)

    @staticmethod
    def format_symbol(symbol: str) -> str:
        """
        Format cryptocurrency string to remove currency exchange from it.
        i.e. BTC-USD -> BTC
        :param symbol: (str) Symbol string to format
        :return: symbol: (str) Formatted symbol string
        """
        currency_postfix = '-USD'
        if currency_postfix in symbol.upper():
            return symbol.replace(currency_postfix, '')
        else:
            return symbol
