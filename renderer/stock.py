import time
import utils
from rgbmatrix.graphics import DrawLine
from constants import ROTATION_RATE, TEXT_SCROLL_DELAY, TEXT_SCROLL_SPEED
from renderer.ticker import TickerRenderer
from data.stock import Stock
from data.color import Color


class StockRenderer(TickerRenderer):
    """
    Renderer for Stock objects

    Arguments:
        matrix (rgbmatrix.RGBMatrix):                       RGBMatrix instance
        canvas (rgbmatrix.Canvas):                          Canvas associated with matrix
        data (data.Data):                                   Data instance

    Attributes:
        stocks (list):                                      List of Stock objects
        market_closed (bool):                               Indicates if stock market is closed
        market_status_color (rgbmatrix.graphics.Color):     Color that indicates stock market's current status
        logo (PIL.Image):                                   Ticker's company logo (if available)
        logo_x_offset (int):                                Ticker's company logo x-coord offset
        logo_y_offset (int):                                Ticker's company logo y-coord offset
    """

    def __init__(self, matrix, canvas, data):
        super().__init__(matrix, canvas, data)
        self.stocks = self.data.stocks

        self.symbol_x = self.coords['symbol']['x']

        self.market_closed = utils.market_closed()
        self.market_status_color = Color.RED if self.market_closed else Color.GREEN

        self.logo = None
        self.logo_x_offset = None
        self.logo_y_offset = self.canvas.height

    def render(self):
        for stock in self.stocks:
            self.populate_data(stock)
            self.canvas.Clear()

            if utils.text_offscreen(self.name, self.canvas.width, self.primary_font.baseline - 1):
                time_started = time.time()
                first_run = True
                self.name_x = 1

                while not self.finished_scrolling:
                    self.canvas.Clear()

                    # Render elements
                    self.render_chart()
                    pos = self.render_name()
                    self.render_market_status()
                    self.render_symbol()
                    self.render_price()
                    self.render_percentage_change()

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
                self.render_name()
                self.render_market_status()
                self.render_symbol()
                self.render_price()
                self.render_percentage_change()

                time.sleep(ROTATION_RATE)

            self.finished_scrolling = False
            self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def populate_data(self, stock: Stock):
        """
        Populate attributes from Stock instance's attributes.
        :param stock: (data.Stock) Stock instance
        """
        super().populate_data(stock)
        self.symbol = stock.symbol
        if stock.logo is not None:
            self.logo = stock.logo
            self.logo_x_offset = utils.center_image(canvas_width=self.canvas.width,
                                                    image_width=self.logo.size[0])[0]

    def render_market_status(self):
        for i in range(2):
            DrawLine(self.canvas, i, 6, i, 11, self.market_status_color)

    def render_logo(self):
        self.canvas.SetImage(self.logo, self.logo_x_offset, self.logo_y_offset)
