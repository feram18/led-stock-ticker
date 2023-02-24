import time

from renderer.ticker import TickerRenderer
from util.utils import load_image_url, align_text, Position


class CryptoRenderer(TickerRenderer):
    """
    Renderer for Crypto objects

    Attributes:
        cryptos (list):         List of Crypto objects
    """

    def __init__(self, matrix, canvas, draw, config, data):
        super().__init__(matrix, canvas, draw, config, data)
        self.cryptos: list = self.data.cryptos

        if self.config.layout.show_logos:
            for crypto in self.cryptos:
                crypto.img = load_image_url(crypto.img_url, tuple(self.coords['crypto']['logo']['size']))

    def render(self):
        for crypto in self.cryptos:
            self.clear()
            if self.coords['options']['full_names']:
                self.render_name(crypto.name)
            if self.coords['options']['image'] and self.config.layout.show_logos:
                self.render_image(crypto.img)
            elif self.coords['options']['history_chart']:
                self.render_chart(crypto.prev_close, crypto.chart_prices, crypto.value_change)
            self.render_price(self.format_price(self.currency, crypto.price), 'crypto')
            self.render_symbol(crypto.symbol.replace('-USD', ''))  # Remove currency exchange
            self.render_percentage_change(crypto.pct_change, crypto.value_change)
            self.matrix.SetImage(self.canvas)
            time.sleep(self.config.rotation_rate)

    def render_symbol(self, symbol: str):
        x = align_text(self.font.getsize(symbol),
                       col_width=self.matrix.width,
                       x=Position(self.coords['crypto']['symbol']['x']))[0]
        x += self.coords['crypto']['symbol']['offset']
        y = self.coords['crypto']['symbol']['y']
        self.draw.text((x, y), symbol, self.text_color, self.font)
