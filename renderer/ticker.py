from abc import ABC, abstractmethod
from rgbmatrix.graphics import DrawText
from renderer.renderer import Renderer
from data.currency import currencies
from data.color import Color
from data.ticker import Ticker
from utils import align_text, Position, convert_currency


class TickerRenderer(Renderer, ABC):
    """
    Renderer for Ticker objects

    Arguments:
        data (data.Data):                                   Data instance

    Attributes:
        coords (dict):                                      Coordinates dictionary
        value_change_color (rgbmatrix.graphics.Color):      Color that indicates if value has increased or decreased
        currency (str):                                     Currency to display prices on
        name (str):                                         Ticker's full name string
        symbol (str):                                       Symbol string
        symbol_x (int):                                     Symbol's x-coord
        price (str):                                        Ticker's price string
        previous_close (float):                             Ticker's previous close price
        pct_change (str):                                   Ticker's percentage change string
        chart_prices (list):                                Ticker's chart data
    """

    def __init__(self, matrix, canvas, config, data):
        super().__init__(matrix, canvas, config)
        self.data = data

        # Load coords
        self.coords = self.config.layout.coords['ticker']

        # Load colors
        self.value_change_color = None

        # Selected currency
        self.currency = self.data.config.currency

        self.name = None
        self.symbol = None
        self.symbol_x = None
        self.symbol_y = self.coords['symbol']['y']
        self.price = None
        self.previous_close = None
        self.pct_change = None
        self.chart_prices = None

    @abstractmethod
    def render(self):
        pass

    def render_name(self, x: int) -> int:
        y = self.coords['name']['y']
        return DrawText(self.canvas, self.secondary_font, x, y, self.text_color, self.name)

    def render_symbol(self):
        DrawText(self.canvas, self.large_font, self.symbol_x, self.symbol_y, self.text_color, self.symbol)

    def render_price(self):
        x = align_text(self.price,
                       x=Position.CENTER,
                       col_width=self.canvas.width,
                       font_width=self.secondary_font.baseline - 1)
        y = self.coords['price']['y']

        DrawText(self.canvas, self.primary_font, x, y, self.text_color, self.price)

    def render_percentage_change(self):
        x = align_text(self.pct_change,
                       x=Position.RIGHT,
                       col_width=self.canvas.width,
                       font_width=self.secondary_font.baseline - 1)
        y = self.coords['value_change']['y']

        DrawText(self.canvas, self.primary_font, x, y, self.value_change_color, self.pct_change)

    def render_chart(self):
        chart_top = self.coords['chart']['y']

        if self.chart_prices:
            min_p, max_p = min(self.chart_prices), max(self.chart_prices)
            x_inc = len(self.chart_prices) / self.canvas.width

            if self.previous_close < min_p:
                prev_close_y = self.canvas.height - 1
            elif self.previous_close > max_p or max_p == min_p:
                prev_close_y = chart_top
            else:
                prev_close_y = int(chart_top + (max_p - self.previous_close) *
                                   ((self.canvas.height - chart_top) / (max_p - min_p)))

            for x in range(self.canvas.width):
                p = self.chart_prices[int(x * x_inc)]
                if max_p == min_p:
                    y = chart_top
                else:
                    y = int(chart_top + (max_p - p) *
                            ((self.canvas.height - chart_top) / (max_p - min_p)))
                step = -1 if y > prev_close_y else 1

                for ys in range(y, prev_close_y + step, step):
                    self.canvas.SetPixel(x,
                                         ys - 1,
                                         self.value_change_color.red,
                                         self.value_change_color.green,
                                         self.value_change_color.blue)
                self.canvas.SetPixel(x,
                                     y - 1,
                                     self.value_change_color.red,
                                     self.value_change_color.green,
                                     self.value_change_color.blue)

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
        if currency in currencies:
            return f'{currencies.get(currency)}{price}'
        else:
            return str(price)

    @staticmethod
    def set_change_color(value_change: float):
        """
        Determines if value has increased or decreased, and returns Color object to match.
        :return: value_change_color: (rgbmatrix.graphics.Color) Value change color
        """
        return Color.RED if value_change < 0 else Color.GREEN
