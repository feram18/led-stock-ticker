import time
from typing import List

from data.stock import Stock
from renderer.ticker import TickerRenderer
from util.color import Color
from util.market_status import MarketStatus
from util.position import Position
from util.utils import load_image_url, align_text


class StockRenderer(TickerRenderer):
    """
    Renderer for Stock objects

    Attributes:
        stocks (List[Stock]):          List of Stock objects
    """

    def __init__(self, matrix, canvas, draw, config, data):
        super().__init__(matrix, canvas, draw, config, data)
        self.stocks: List[Stock] = self.data.stocks
        self.symbol_x: int = 0

        if self.config.layout.show_logos:
            for stock in self.stocks:
                stock.img = load_image_url(stock.logo_url, tuple(self.coords['stock']['logo']['size']))

    def render(self):
        for stock in self.stocks:
            self.clear()
            if self.coords['options']['full_names']:
                self.render_name(stock.name)
            if self.coords['options']['image'] and self.config.layout.show_logos:
                self.render_image(stock.img)
            elif self.coords['options']['history_chart']:
                self.render_chart(stock.prev_close, stock.chart_prices, stock.value_change)
            self.render_price(self.format_price(self.currency, stock.price), 'stock')
            self.render_symbol(stock.symbol)
            self.render_market_status()
            self.render_percentage_change(stock.pct_change, stock.value_change)
            self.matrix.SetImage(self.canvas)
            time.sleep(self.config.rotation_rate)

    def render_symbol(self, symbol: str):
        pos = Position(self.coords['stock']['symbol']['x'])
        offset = self.coords['stock']['market_status']['width'] if pos is Position.CENTER else 0
        self.symbol_x = align_text(self.font.getsize(symbol),
                                   col_width=self.matrix.width,
                                   x=pos)[0]
        x = self.symbol_x + self.coords['stock']['symbol']['offset'] + offset
        y = self.coords['stock']['symbol']['y']
        self.draw.text((x, y), symbol, self.text_color, self.font)

    def render_market_status(self):
        ms_coords = self.coords['stock']['market_status']
        color = Color.RED if self.data.market_status is MarketStatus.CLOSED else Color.GREEN
        x = self.symbol_x + ms_coords['offset']
        self.draw.line(((x, ms_coords['top']), (x, ms_coords['bottom'])), color, ms_coords['width'])
