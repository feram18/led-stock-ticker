import utils
from abc import ABC, abstractmethod
from rgbmatrix.graphics import DrawText
from renderer.renderer import Renderer
from data.currency import currencies
from data.color import Color
from data.ticker import Ticker


class TickerRenderer(Renderer, ABC):
    """
    Renderer for Ticker objects

    Arguments:
        matrix (rgbmatrix.RGBMatrix):                       RGBMatrix instance
        canvas (rgbmatrix.Canvas):                          Canvas associated with matrix
        data (data.Data):                                   Data instance

    Attributes:
        coords (dict):                                      Coordinates dictionary
        text_color (rgbmatrix.graphics.Color):              Main text color
        value_change_color (rgbmatrix.graphics.Color):      Color that indicates if value has increased or decreased
        fonts (dict):                                       Fonts dictionary
        primary_font (rgbmatrix.graphics.Font):             Primary Font object
        secondary_font (rgbmatrix.graphics.Font):           Secondary Font object
        large_font (rgbmatrix.graphics.Font):               Large Font object
        currency (str):                                     Currency to display prices on
        name (str):                                         Ticker's full name string
        name_x (int):                                       Ticker's full name's x-coord
        name_y (int):                                       Ticker's full name's y-coord
        symbol (str):                                       Symbol string
        symbol_x (int):                                     Symbol's x-coord
        symbol_y (int):                                     Symbol's y-coord
        price (str):                                        Ticker's price string
        price_x (int):                                      Ticker's price x-coord
        price_y (int):                                      Ticker's price y-coord
        previous_close (float):                             Ticker's previous close price
        value_change (str):                                 Ticker's value change string
        value_change_x (int):                               Ticker's value change x-coord
        value_change_y (int):                               Ticker's value change y-coord
        chart_prices (list):                                Ticker's chart data
        chart_y (int):                                      Ticker's chart max y-coord
        finished_scrolling (bool):                          Indicates if scrolling text has finished scrolling
    """

    def __init__(self, matrix, canvas, data):
        super().__init__(matrix, canvas)
        self.data = data

        # Load coords
        self.coords = self.data.config.layout['coords']['ticker']

        # Load colors
        self.text_color = Color.WHITE
        self.value_change_color = None

        # Load fonts
        self.fonts = self.data.config.layout['fonts']
        self.primary_font = utils.load_font(self.fonts['tom_thumb'])
        self.secondary_font = utils.load_font(self.fonts['4x6'])
        self.large_font = utils.load_font(self.fonts['6x9'])

        # Selected currency
        self.currency = self.data.config.currency

        self.name = None
        self.name_x = self.coords['name']['x']
        self.name_y = self.coords['name']['y']

        self.symbol = None
        self.symbol_x = None
        self.symbol_y = self.coords['symbol']['y']

        self.price = None
        self.price_x = self.coords['price']['x']
        self.price_y = self.coords['price']['y']

        self.previous_close = None

        self.value_change = None
        self.value_change_x = self.coords['value_change']['x']
        self.value_change_y = self.coords['value_change']['y']

        self.chart_prices = None
        self.chart_y = self.coords['chart']['y']

        self.finished_scrolling = False

    @abstractmethod
    def render(self):
        pass

    def render_name(self):
        return DrawText(self.canvas,
                        self.primary_font,
                        self.name_x,
                        self.name_y,
                        self.text_color,
                        self.name)

    def render_symbol(self):
        DrawText(self.canvas,
                 self.large_font,
                 self.symbol_x,
                 self.symbol_y,
                 self.text_color,
                 self.symbol)

    def render_price(self):
        DrawText(self.canvas,
                 self.secondary_font,
                 self.price_x,
                 self.price_y,
                 self.text_color,
                 self.price)

    def render_percentage_change(self):
        DrawText(self.canvas,
                 self.secondary_font,
                 self.value_change_x,
                 self.value_change_y,
                 self.value_change_color,
                 self.value_change)

    def render_chart(self):
        if self.chart_prices:
            min_p, max_p = min(self.chart_prices), max(self.chart_prices)
            x_inc = len(self.chart_prices) / self.canvas.width

            if self.previous_close < min_p:
                prev_close_y = self.canvas.height - 1
            elif self.previous_close > max_p or max_p == min_p:
                prev_close_y = self.chart_y
            else:
                prev_close_y = int(self.chart_y + (max_p - self.previous_close) *
                                   ((self.canvas.height - self.chart_y) / (max_p - min_p)))

            for x in range(self.canvas.width):
                p = self.chart_prices[int(x * x_inc)]
                if max_p == min_p:
                    y = self.chart_y
                else:
                    y = int(self.chart_y + (max_p - p) *
                            ((self.canvas.height - self.chart_y) / (max_p - min_p)))
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
        self.name = ticker.name
        self.price = self.format_price(self.currency, ticker.current_price)
        self.price_x = utils.align_text_center(string=self.price,
                                               canvas_width=self.canvas.width,
                                               font_width=self.primary_font.baseline - 1)[0]
        if self.currency == 'USD':
            self.previous_close = ticker.previous_close
        else:  # Convert back to USD for chart calculations purposes
            self.previous_close = utils.convert_currency(self.currency,
                                                         'USD',
                                                         ticker.previous_close)
        self.value_change = ticker.pct_change
        self.value_change_x = utils.align_text_right(self.value_change,
                                                     self.canvas.width,
                                                     self.primary_font.baseline - 1)
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
