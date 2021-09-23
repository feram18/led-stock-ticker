import time
import utils
from rgbmatrix.graphics import DrawText, DrawLine
from constants import ROTATION_RATE, TEXT_SCROLL_DELAY, TEXT_SCROLL_SPEED
from data.crypto import Crypto
from data.stock import Stock
from data.ticker import Ticker
from data.currency import currencies
from data.color import Color


class TickerRenderer:
    """
    Render Tickers
    Arguments:
        matrix (rgbmatrix.RGBMatrix):                       RGBMatrix instance
        canvas (rgbmatrix.Canvas):                          Canvas associated with matrix
        data (data.Data):                                   Data instance
    Attributes:
        coords (dict):                                      Coordinates dictionary
        text_color (rgbmatrix.graphics.Color):              Main text color
        value_change_color (rgbmatrix.graphics.Color):      Color that indicates if value has increased or decreased
        market_status_color (rgbmatrix.graphics.Color):     Color that indicates stock market's current status
        fonts (dict):                                       Fonts dictionary
        primary_font (rgbmatrix.graphics.Font):             Primary Font object
        secondary_font (rgbmatrix.graphics.Font):           Secondary Font object
        large_font (rgbmatrix.graphics.Font):               Large Font object
        tickers (list):                                     List of Ticker instances
        currency (str):                                     Currency to display prices on
        market_closed (bool):                               Indicates if stock market is closed
        name (str):                                         Ticker's full name string
        name_x (int):                                       Ticker's full name's x-coord
        name_y (int):                                       Ticker's full name's y-coord
        ticker_ (str):                                      Ticker string
        ticker_x (int):                                     Ticker's x-coord
        ticker_y (int):                                     Ticker's y-coord
        price (str):                                        Ticker's price string
        price_x (int):                                      Ticker's price x-coord
        price_y (int):                                      Ticker's price y-coord
        prev_close_price (float):                           Ticker's previous close price
        value_change (str):                                 Ticker's value change string
        value_change_x (int):                               Ticker's value change x-coord
        value_change_y (int):                               Ticker's value change y-coord
        chart_prices (list):                                Ticker's chart data
        chart_y (int):                                      Ticker's chart max y-coord
        logo (PIL.Image):                                   Ticker's company logo (if available)
        logo_x_offset (int):                                Ticker's company logo x-coord offset
        logo_y_offset (int):                                Ticker's company logo y-coord offset
        finished_scrolling (bool):                          Indicates if scrolling text has finished scrolling
    """

    def __init__(self, matrix, canvas, data):
        self.matrix = matrix
        self.canvas = canvas
        self.data = data

        # Load coords
        self.coords = self.data.config.layout['coords']['ticker']

        # Load colors
        self.text_color = Color.WHITE
        self.value_change_color = None
        self.market_status_color = None

        # Load fonts
        self.fonts = self.data.config.layout['fonts']
        self.primary_font = utils.load_font(self.fonts['tom_thumb'])
        self.secondary_font = utils.load_font(self.fonts['4x6'])
        self.large_font = utils.load_font(self.fonts['6x9'])

        # Stock/Cryptocurrency data
        self.tickers = self.data.tickers

        # User's selected currency
        self.currency = self.data.config.currency

        # Set strings and coords
        self.market_closed = None

        self.name = None
        self.name_x = self.coords['name']['x']
        self.name_y = self.coords['name']['y']

        self.ticker_ = None
        self.ticker_x = self.coords['ticker']['x']
        self.ticker_y = self.coords['ticker']['y']

        self.price = None
        self.price_x = self.coords['price']['x']
        self.price_y = self.coords['price']['y']

        self.prev_close_price = None

        self.value_change = None
        self.value_change_x = self.coords['value_change']['x']
        self.value_change_y = self.coords['value_change']['y']

        self.chart_prices = None
        self.chart_y = self.coords['chart']['y']

        self.logo = None
        self.logo_x_offset = None
        self.logo_y_offset = self.canvas.height

        self.finished_scrolling = False

    def render(self):
        for ticker in self.tickers:
            self.set_data(ticker)
            self.canvas.Clear()

            if utils.text_offscreen(self.name, self.canvas.width, self.primary_font.baseline - 1):
                time_started = time.time()
                first_run = True
                self.name_x = 1

                while not self.finished_scrolling:
                    self.canvas.Clear()

                    # Render elements
                    self.render_chart()
                    pos = self.render_full_name()
                    self.render_market_status()
                    self.render_ticker()
                    self.render_price()
                    self.render_value_change()

                    if first_run:
                        time.sleep(TEXT_SCROLL_DELAY)
                        first_run = False

                    time.sleep(TEXT_SCROLL_SPEED)

                    self.name_x = utils.scroll_text(self.canvas.width, self.name_x, pos)

                    if time.time() - time_started >= ROTATION_RATE:
                        self.finished_scrolling = True
            else:
                self.name_x = utils.align_text_center(string=self.name,
                                                      canvas_width=self.canvas.width,
                                                      font_width=self.primary_font.baseline - 1)[0]

                # Render elements
                self.render_chart()
                self.render_full_name()
                self.render_market_status()
                self.render_ticker()
                self.render_price()
                self.render_value_change()

                time.sleep(ROTATION_RATE)

            self.finished_scrolling = False
            self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def set_data(self, ticker: Ticker):
        """
        Populate variables from Ticker instance's attributes.
        :param ticker: (data.Ticker) Ticker instance
        """
        self.name = ticker.name
        self.market_closed = self.market_status_closed(ticker)
        self.market_status_color = self.set_market_status_color(self.market_closed)
        self.ticker_ = self.format_ticker(ticker.ticker) if isinstance(ticker, Crypto) else ticker.ticker
        self.price = self.format_price(self.currency, ticker.current_price)
        self.price_x = utils.align_text_center(string=self.price,
                                               canvas_width=self.canvas.width,
                                               font_width=self.primary_font.baseline - 1)[0]
        if self.currency == 'USD':
            self.prev_close_price = ticker.prev_close_price
        else:  # Convert back to USD for chart calculations purposes
            self.prev_close_price = utils.convert_currency(self.currency,
                                                           'USD',
                                                           ticker.prev_close_price)
        self.value_change = ticker.pct_change
        self.value_change_x = utils.align_text_right(self.value_change,
                                                     self.canvas.width,
                                                     self.primary_font.baseline - 1)
        self.value_change_color = self.set_change_color(ticker.value_change)
        self.chart_prices = ticker.chart_prices
        if isinstance(ticker, Stock) and ticker.logo is not None:
            self.logo = ticker.logo
            self.logo_x_offset = utils.center_image(canvas_width=self.canvas.width,
                                                    image_width=self.logo.size[0])[0]

    def render_market_status(self):
        for i in range(2):
            DrawLine(self.canvas, i, 6, i, 11, self.market_status_color)

    def render_full_name(self):
        return DrawText(self.canvas,
                        self.primary_font,
                        self.name_x,
                        self.name_y,
                        self.text_color,
                        self.name)

    def render_ticker(self):
        DrawText(self.canvas,
                 self.large_font,
                 self.ticker_x,
                 self.ticker_y,
                 self.text_color,
                 self.ticker_)

    def render_price(self):
        DrawText(self.canvas,
                 self.secondary_font,
                 self.price_x,
                 self.price_y,
                 self.text_color,
                 self.price)

    def render_value_change(self):
        DrawText(self.canvas,
                 self.secondary_font,
                 self.value_change_x,
                 self.value_change_y,
                 self.value_change_color,
                 self.value_change)

    def render_logo(self):
        self.canvas.SetImage(self.logo, self.logo_x_offset, self.logo_y_offset)

    def render_chart(self):
        if self.chart_prices:
            min_p, max_p = min(self.chart_prices), max(self.chart_prices)
            x_inc = len(self.chart_prices) / self.canvas.width

            if self.prev_close_price < min_p:
                prev_close_y = self.canvas.height - 1
            elif self.prev_close_price > max_p or max_p == min_p:
                prev_close_y = self.chart_y
            else:
                if max_p == min_p:
                    prev_close_y = self.chart_y
                else:
                    prev_close_y = int(self.chart_y + (max_p - self.prev_close_price) *
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

    @staticmethod
    def format_ticker(ticker: str) -> str:
        """
        Format cryptocurrency string to remove currency exchange from it.
        i.e. BTC-USD -> BTC
        :param ticker: (str) Ticker string to format
        :return: ticker: (str) Formatted ticker string
        """
        currency_postfix = '-USD'
        if currency_postfix in ticker.upper():
            return ticker.replace(currency_postfix, '')
        else:
            return ticker

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

    @staticmethod
    def set_market_status_color(market_closed_: bool):
        """
        Returns red Color object if stock market is closed, and green if open.
        :return: market_status_color: (rgbmatrix.graphics.Color) Market status color
        """
        return Color.RED if market_closed_ else Color.GREEN

    @staticmethod
    def market_status_closed(ticker: Ticker) -> bool:
        """
        Determine if the stock market is currently closed. If ticker is a crypto, market is always open.
        :param ticker: (data.Ticker) Ticker instance
        :return: status: (bool) Market Closed
        """
        return False if isinstance(ticker, Crypto) else utils.market_closed()
