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
        x, y = align_text(self.primary_font.getsize(name),
                          self.matrix.width,
                          self.matrix.height,
                          Position.CENTER,
                          Position.TOP)
        if off_screen(self.matrix.width, self.primary_font.getsize(name)[0]):
            self.scroll_text(name, self.primary_font, self.text_color, Color.BLACK, (1, y))
        else:
            self.draw.text((x, y), name, self.text_color, self.primary_font)

    @abstractmethod
    def render_symbol(self, symbol: str):
        pass

    def render_price(self, price: str):
        x = align_text(self.primary_font.getsize(price),
                       col_width=self.matrix.width,
                       x=Position.CENTER)[0]
        y = self.coords['price']['y']
        self.draw.text((x, y), price, self.text_color, self.primary_font)

    def render_percentage_change(self, pct_change: str, value_change: float):
        x = align_text(self.primary_font.getsize(pct_change),
                       col_width=self.matrix.width,
                       x=Position.RIGHT)[0]
        y = self.coords['value_change']['y']

        color = self.set_change_color(value_change)
        self.draw.text((x, y), pct_change, color, self.primary_font)

    def render_chart(self, prev_close: float, prices: list, value_change: float):
        chart_top = self.coords['chart']['y']
        color = self.set_change_color(value_change)

        if prices:
            min_p, max_p = min(prices), max(prices)
            x_inc = len(prices) / self.matrix.width

            if prev_close < min_p:
                prev_close_y = self.matrix.height - 1
            elif prev_close > max_p or max_p == min_p:
                prev_close_y = chart_top
            else:
                prev_close_y = int(chart_top + (max_p - prev_close) *
                                   ((self.matrix.height - chart_top) / (max_p - min_p)))

            for x in range(self.matrix.width):
                p = prices[int(x * x_inc)]
                if max_p == min_p:
                    y = chart_top
                else:
                    y = int(chart_top + (max_p - p) *
                            ((self.matrix.height - chart_top) / (max_p - min_p)))
                step = -1 if y > prev_close_y else 1

                for ys in range(y, prev_close_y + step, step):
                    self.draw.point((x, ys - 1), color)
                self.draw.point((x, y - 1), color)

    def render_logo(self, logo: Image):
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
            return f'{CURRENCIES.get(currency)}{price}'
        return str(price)

    @staticmethod
    def set_change_color(value_change: float) -> tuple:
        """
        Determines if value has increased or decreased, and returns Color object to match.
        :return: value_change_color: (tuple) Value change color
        """
        return Color.RED if value_change < 0 else Color.GREEN
