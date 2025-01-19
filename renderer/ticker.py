import logging
from abc import ABC, abstractmethod

from PIL import Image

from data.currency import CURRENCIES
from renderer.renderer import Renderer
from util.color import Color
from util.position import Position
from util.utils import align_text, off_screen, align_image


class TickerRenderer(Renderer, ABC):
    """
    Renderer for Ticker objects

    Arguments:
        data (data.Data):       Data instance

    Attributes:
        coords (dict):          Coordinates dictionary
        currency (str):         Currency to display prices on
    """

    def __init__(self, matrix, canvas, draw, config, data):
        super().__init__(matrix, canvas, draw, config)
        self.data = data
        self.coords: dict = self.config.layout.coords['ticker']
        self.currency: str = self.data.config.currency

    @abstractmethod
    def render(self):
        pass

    def render_name(self, name: str):
        x, y = align_text(self.font.getsize(name),
                          self.matrix.width,
                          self.matrix.height,
                          Position.CENTER,
                          Position.TOP)
        if off_screen(self.matrix.width, self.font.getsize(name)[0]):
            self.scroll_text(name, self.font, self.text_color, Color.BLACK, (1, y))
        else:
            self.draw.text((x, y), name, self.text_color, self.font)

    def render_price(self, price: str, ticker_type: str):
        y = self.coords[ticker_type]['price']['y']
        if off_screen(self.matrix.width, self.font.getsize(price)[0]):
            self.scroll_text(price, self.font, self.text_color, Color.BLACK, (1, y))
        else:
            x = align_text(self.font.getsize(price),
                           col_width=self.matrix.width,
                           x=Position(self.coords[ticker_type]['price']['x']))[0]
            x += self.coords[ticker_type]['price']['offset']
            self.draw.text((x, y), price, self.text_color, self.font)

    def render_percentage_change(self, pct_change: str, value_change: float):
        x = align_text(self.font.getsize(pct_change),
                       col_width=self.matrix.width,
                       x=Position(self.coords['change_pct']['x']))[0]
        y = self.coords['change_pct']['y']

        color = self.set_change_color(value_change)
        self.draw.text((x, y), pct_change, color, self.font)

    def render_chart(self, prev_close: float, prices: list, value_change: float):
        chart_top = self.coords['chart']['y']
        chart_height = self.matrix.height - chart_top - 1
        color = self.set_change_color(value_change)

        if prices:
            try:
                max_price = max(prices)
                min_price = min(prices)
                price_range = max_price - min_price

                num_points = len(prices)
                x_step = self.matrix.width / (num_points - 1)

                line_points = [(i * x_step, chart_top + chart_height * (1 - (price - min_price) / price_range))
                               for i, price in enumerate(prices)]

                fill_points = ([(0, chart_top + chart_height)] + line_points +
                               [(self.matrix.width, chart_top + chart_height), (0, chart_top + chart_height)])

                self.draw.polygon(fill_points, fill=color)
                self.draw.line(line_points, fill=color, width=1)
            except ValueError as e:
                logging.warning('Unable to render chart', e)

    def render_image(self, logo: Image):
        if logo:
            x, y = align_image(logo,
                               self.matrix.width,
                               self.matrix.height,
                               Position.CENTER,
                               Position.BOTTOM)
            self.canvas.paste(logo, (x, y))

    @staticmethod
    def format_price(currency: str, price: float) -> str:
        """
        Format price string to show appropriate currency symbol.
        i.e. USD -> $, EUR -> €
        :param currency: (str) Currency
        :param price: (float) Price value
        :return: price: (str) Formatted price string
        """
        if currency in CURRENCIES:
            return f'{CURRENCIES.get(currency)}{price:.6f}'.rstrip('0').rstrip('.')
        return f'{price:.6f}'.rstrip('0').rstrip('.')

    @staticmethod
    def set_change_color(value_change: float) -> tuple:
        """
        Determines if value has increased or decreased, and returns Color object to match.
        :return: value_change_color: (tuple) Value change color
        """
        return Color.GREEN if value_change > 0.00 else Color.RED
