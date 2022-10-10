from abc import ABC, abstractmethod

from data.currency import CURRENCIES
from data.ticker import Ticker
from renderer.renderer import Renderer
from util.color import Color
from util.position import Position
from util.utils import align_text, convert_currency, off_screen


class TickerRenderer(Renderer, ABC):
    """
    Renderer for Ticker objects

    Arguments:
        data (data.Data):                   Data instance

    Attributes:
        coords (dict):                      Coordinates dictionary
        value_change_color (tuple):         Color that indicates if value has increased or decreased
        currency (str):                     Currency to display prices on
        name (str):                         Ticker's full name string
        symbol (str):                       Symbol string
        price (str):                        Ticker's price string
        previous_close (float):              Ticker's previous close price
        pct_change (str):                   Ticker's percentage change string
        chart_prices (list):                Ticker's chart data
    """

    def __init__(self, matrix, canvas, draw, config, data):
        super().__init__(matrix, canvas, draw, config)
        self.data = data
        self.coords: dict = self.config.layout.coords['ticker']
        self.value_change_color: tuple = Color.GREEN
        self.currency: str = self.data.config.currency
        self.name: str = ''
        self.symbol: str = ''
        self.price: str = '0.0'
        self.previous_close: float = 0.0
        self.pct_change: str = '0.0%'
        self.chart_prices: list = []

    @abstractmethod
    def render(self):
        pass

    def render_name(self):
        x, y = align_text(self.secondary_font.getsize(self.name),
                          self.matrix.width,
                          self.matrix.height,
                          Position.CENTER,
                          Position.TOP)

        if off_screen(self.matrix.width, self.secondary_font.getsize(self.name)[0]):
            self.scroll_text(self.name, self.secondary_font, self.text_color, Color.BLACK, (1, y))
        else:
            self.draw.text((x, y), self.name, self.text_color, self.secondary_font)

    @abstractmethod
    def render_symbol(self):
        ...

    def render_price(self):
        x = align_text(self.primary_font.getsize(self.price),
                       col_width=self.matrix.width,
                       x=Position.CENTER)[0]
        y = self.coords['price']['y']
        self.draw.text((x, y), self.price, self.text_color, self.primary_font)

    def render_percentage_change(self):
        x = align_text(self.primary_font.getsize(self.pct_change),
                       col_width=self.matrix.width,
                       x=Position.RIGHT)[0]
        y = self.coords['value_change']['y']
        self.draw.text((x, y), self.pct_change, self.value_change_color, self.primary_font)

    def render_chart(self):
        chart_top = self.coords['chart']['y']

        if self.chart_prices:
            min_p, max_p = min(self.chart_prices), max(self.chart_prices)
            x_inc = len(self.chart_prices) / self.matrix.width

            if self.previous_close < min_p:
                prev_close_y = self.matrix.height - 1
            elif self.previous_close > max_p or max_p == min_p:
                prev_close_y = chart_top
            else:
                prev_close_y = int(chart_top + (max_p - self.previous_close) *
                                   ((self.matrix.height - chart_top) / (max_p - min_p)))

            for x in range(self.matrix.width):
                p = self.chart_prices[int(x * x_inc)]
                if max_p == min_p:
                    y = chart_top
                else:
                    y = int(chart_top + (max_p - p) *
                            ((self.matrix.height - chart_top) / (max_p - min_p)))
                step = -1 if y > prev_close_y else 1

                for ys in range(y, prev_close_y + step, step):
                    self.draw.point((x, ys - 1), self.value_change_color)
                self.draw.point((x, y - 1), self.value_change_color)

    def populate_data(self, ticker: Ticker):
        """
        Populate attributes from Ticker instance's attributes.
        :param ticker: (data.Ticker) Ticker instance
        """
        self.symbol = ticker.symbol
        self.name = ticker.name
        self.price = self.format_price(self.currency, ticker.price)
        self.previous_close = ticker.prev_close
        if self.currency != 'USD':  # Convert back to USD for chart calculations purposes
            self.previous_close = convert_currency(self.currency, 'USD', ticker.prev_close)
        self.pct_change = ticker.pct_change
        self.value_change_color = self.set_change_color(ticker.value_change)
        self.chart_prices = ticker.chart_prices

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
