import time
from typing import List

from data.stock import Stock
from renderer.ticker import TickerRenderer
from util.color import Color
from util.market_status import MarketStatus
from util.utils import load_image_url, convert_currency


class StockRenderer(TickerRenderer):
    """
    Renderer for Stock objects

    Attributes:
        stocks (List[Stock]):          List of Stock objects
    """

    def __init__(self, matrix, canvas, draw, config, data):
        super().__init__(matrix, canvas, draw, config, data)
        self.stocks: List[Stock] = self.data.stocks

        if self.config.layout.show_logos:
            for stock in self.stocks:
                stock.logo = load_image_url(stock.logo_url, tuple(self.coords['logo']['size']))

    def render(self):
        for stock in self.stocks:
            previous_close = stock.prev_close
            if self.currency != 'USD':  # Convert back to USD for chart calculations purposes
                previous_close = convert_currency(self.currency, 'USD', stock.prev_close)

            self.clear()
            self.render_name(stock.name)
            self.render_market_status()
            self.render_symbol(stock.symbol)
            self.render_price(self.format_price(self.currency, stock.price))
            self.render_percentage_change(stock.pct_change, stock.value_change)
            if self.config.layout.show_logos:
                self.render_logo(stock.logo)
            else:
                self.render_chart(previous_close, stock.chart_prices, stock.value_change)
            self.matrix.SetImage(self.canvas)
            time.sleep(self.config.rotation_rate)

    def render_symbol(self, symbol: str):
        x = self.coords['stock']['symbol']['x']
        y = self.coords['stock']['symbol']['y']
        self.draw.text((x, y), symbol, self.text_color, self.large_font)

    def render_market_status(self):
        ms_coords = self.coords['stock']['market_status']
        color = Color.RED if self.data.market_status is MarketStatus.CLOSED else Color.GREEN
        self.draw.line(((0, ms_coords['top']), (0, ms_coords['bottom'])), color, ms_coords['width'])
