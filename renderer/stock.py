import time

from PIL import Image

from data.stock import Stock
from renderer.ticker import TickerRenderer
from util.color import Color
from util.position import Position
from util.utils import market_closed, align_image, load_image_url


class StockRenderer(TickerRenderer):
    """
    Renderer for Stock objects

    Attributes:
        stocks (list):          List of Stock objects
        ms_color (tuple):       Market status color indicator
        logo (PIL.Image):       Ticker's logo image
    """

    def __init__(self, matrix, canvas, draw, config, data):
        super().__init__(matrix, canvas, draw, config, data)
        self.stocks: list = self.data.stocks
        self.ms_color: tuple = Color.RED if market_closed() else Color.GREEN
        self.logo: Image = None

    def render(self):
        for stock in self.stocks:
            self.populate_data(stock)
            self.clear()
            self.render_name()
            self.render_market_status()
            self.render_symbol()
            self.render_price()
            self.render_percentage_change()
            if self.coords['options']['chart']:
                self.render_chart()
            elif self.coords['options']['logo']:
                self.render_logo()
            self.matrix.SetImage(self.canvas)
            time.sleep(self.config.rotation_rate)

    def populate_data(self, stock: Stock):
        """
        Populate attributes from Stock instance's attributes.
        :param stock: (data.Stock) Stock instance
        """
        super().populate_data(stock)
        self.logo = load_image_url(stock.logo_url, tuple(self.coords['logo']['size']))

    def render_symbol(self):
        x = self.coords['stock']['symbol']['x']
        y = self.coords['stock']['symbol']['y']
        self.draw.text((x, y), self.symbol, self.text_color, self.large_font)

    def render_market_status(self):
        ms_coords = self.coords['stock']['market_status']
        self.draw.line(((0, ms_coords['top']), (0, ms_coords['bottom'])), self.ms_color, ms_coords['width'])

    def render_logo(self):
        x, y = align_image(self.logo,
                           self.matrix.width,
                           self.matrix.height,
                           Position.CENTER,
                           Position.BOTTOM)
        self.canvas.paste(self.logo, (x, y))
