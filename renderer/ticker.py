from constants import ROTATION_RATE, TEXT_SCROLL_DELAY, TEXT_SCROLL_SPEED
from rgbmatrix import graphics
import utils as u
import time


class TickerRenderer:
    def __init__(self, matrix, canvas, data):
        self.matrix = matrix
        self.canvas = canvas

        # Load coords
        self.coords = data.config.layout["coords"]["ticker"]

        # Load colors
        self.colors = data.config.colors["ticker"]
        self.main_color = u.load_color(self.colors["main"])
        self.secondary_color = u.load_color(self.colors["secondary"])

        # Load fonts
        self.fonts = data.config.layout["fonts"]

        self.FONT_TOM_THUMB = self.fonts["tom_thumb"]
        self.primary_font = u.load_font(self.FONT_TOM_THUMB["path"])

        self.FONT_4X6 = self.fonts["4x6"]
        self.secondary_font = u.load_font(self.FONT_4X6["path"])

        self.FONT_6X9 = self.fonts["6x9"]
        self.large_font = u.load_font(self.FONT_6X9["path"])

        # Stock/Cryptocurrency data
        self.tickers = data.tickers

        self.currency = data.config.currency

        self.name = None
        self.name_x = None
        self.name_y = None

        self.ticker_ = None
        self.ticker_x = None
        self.ticker_y = None

        self.price = None
        self.price_x = None
        self.price_y = None

        self.value_and_pct_change = None
        self.value_x = None
        self.value_y = None

        self.value_indicator_color = None

        self.finished_scrolling = False

    def render(self):
        for ticker in self.tickers:
            self.set_data(ticker)
            self.canvas.Clear()

            if u.text_offscreen(self.name, self.canvas.width, self.FONT_TOM_THUMB["width"]):
                time_started = time.time()
                first_run = True
                self.name_x = 1

                while self.finished_scrolling is False:
                    self.canvas.Clear()

                    # Render elements
                    pos = self.__render_full_name()
                    self.__render_ticker()
                    self.__render_price()
                    self.__render_value_and_pct_change()

                    if first_run is True:
                        time.sleep(TEXT_SCROLL_DELAY)
                        first_run = False

                    time.sleep(TEXT_SCROLL_SPEED)

                    self.name_x = self.__update_text_position(self.name_x, pos)

                    if time.time() - time_started >= ROTATION_RATE:
                        self.finished_scrolling = True
            else:
                self.name_x = u.align_center(self.name, (self.canvas.width / 2), self.FONT_TOM_THUMB["width"])

                # Render elements
                self.__render_full_name()
                self.__render_ticker()
                self.__render_price()
                self.__render_value_and_pct_change()

                time.sleep(ROTATION_RATE)

            self.finished_scrolling = False
            self.canvas = self.matrix.SwapOnVSync(self.canvas)

    # Set Ticker's data
    def set_data(self, ticker):
        self.name = ticker.name
        self.name_y = self.coords["name"]["y"]

        self.ticker_ = self.format_ticker(ticker.ticker)
        self.ticker_x = self.coords["ticker"]["x"]
        self.ticker_y = self.coords["ticker"]["y"]

        self.price = "${}".format(ticker.current_price)
        self.price_x = u.align_right(self.price, self.canvas.width, self.FONT_TOM_THUMB["width"])
        self.price_y = self.coords["price"]["y"]

        self.value_and_pct_change = "{} {}".format(ticker.value_change, ticker.percentage_change)
        self.value_x = u.align_center(self.value_and_pct_change, (self.canvas.width / 2), self.FONT_TOM_THUMB["width"])
        self.value_y = self.coords["value_and_pct_change"]["y"]

        self.value_indicator_color = self.set_indicator_color(float(ticker.value_change))

    def __render_full_name(self):
        return graphics.DrawText(self.canvas, self.primary_font, self.name_x, self.name_y, self.main_color, self.name)

    def __render_ticker(self):
        return graphics.DrawText(self.canvas,
                                 self.large_font,
                                 self.ticker_x,
                                 self.ticker_y,
                                 self.main_color,
                                 self.ticker_)

    def __render_price(self):
        return graphics.DrawText(self.canvas,
                                 self.primary_font,
                                 self.price_x,
                                 self.price_y,
                                 self.main_color,
                                 self.price)

    def __render_value_and_pct_change(self):
        return graphics.DrawText(self.canvas,
                                 self.primary_font,
                                 self.value_x,
                                 self.value_y,
                                 self.value_indicator_color,
                                 self.value_and_pct_change)

    def __update_text_position(self, full_name_x: int, pos: int) -> int:
        """
        Update x-coord on scrolling text
        :param full_name_x: int
        :param pos: int
        :return: x_coord: int
        """
        if full_name_x + pos < 1:
            return self.canvas.width
        else:
            return full_name_x - 1

    def format_ticker(self, ticker: str) -> str:
        """
        Format cryptocurrency to remove currency value from it.
        i.e. BTC/USD -> BTC
        :param ticker: str
        :return: ticker: str
        """
        currency_postfix = f"/{self.currency}"
        if currency_postfix.upper() in ticker:
            return ticker.replace(currency_postfix, "")
        else:
            return ticker

    def set_indicator_color(self, value_change: float):
        """
        Determines if value has increased or decreased, and returns Color object to match.
        i.e. Red if value has decreased, Green if color has increased.
        :param value_change: int
        :return: value_indicator_color: Color
        """
        if value_change < 0:
            return u.load_color(self.colors["decrease"])
        else:
            return u.load_color(self.colors["increase"])
