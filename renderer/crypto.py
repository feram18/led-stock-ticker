import time
from renderer.ticker import TickerRenderer
from data.crypto import Crypto
from data.position import Position
from utils import text_offscreen, scroll_text, align_text
from constants import ROTATION_RATE, TEXT_SCROLL_DELAY, TEXT_SCROLL_SPEED


class CryptoRenderer(TickerRenderer):
    """
    Renderer for Crypto objects

    Attributes:
        cryptos (list):         List of Crypto objects
        symbol_x (int):         Crypto's symbol x-coord
    """

    def __init__(self, matrix, canvas, config, data):
        super().__init__(matrix, canvas, config, data)
        self.cryptos = self.data.cryptos
        self.symbol_x = 0

    def render(self):
        for crypto in self.cryptos:
            self.populate_data(crypto)
            self.canvas.Clear()

            finished_scrolling = False
            if text_offscreen(self.name, self.canvas.width, self.primary_font.baseline - 1):
                time_started = time.time()
                first_run = True
                x = 1

                while not finished_scrolling:
                    self.canvas.Clear()

                    # Render elements
                    self.render_chart()
                    pos = self.render_name(x)
                    self.render_symbol()
                    self.render_price()
                    self.render_percentage_change()

                    if first_run:
                        time.sleep(TEXT_SCROLL_DELAY)
                        first_run = False

                    time.sleep(TEXT_SCROLL_SPEED)

                    x = scroll_text(self.canvas.width, x, pos)

                    if time.time() - time_started >= ROTATION_RATE:
                        finished_scrolling = True
            else:
                # Render elements
                self.render_chart()
                x = align_text(text=self.name,
                               x=Position.CENTER,
                               col_width=self.canvas.width,
                               font_width=self.secondary_font.baseline - 1)
                self.render_name(x)
                self.render_symbol()
                self.render_price()
                self.render_percentage_change()

                time.sleep(ROTATION_RATE)

            self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def populate_data(self, crypto: Crypto):
        """
        Populate attributes from Crypto instance's attributes.
        :param crypto: (data.Crypto) Crypto instance
        """
        super().populate_data(crypto)
        self.symbol = self.symbol.replace('-USD', '')  # Remove currency exchange
