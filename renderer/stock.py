import time
from rgbmatrix.graphics import DrawLine
from renderer.ticker import TickerRenderer
from data.stock import Stock
from util.utils import market_closed, text_offscreen, scroll_text, align_image, align_text
from util.position import Position
from util.color import Color
from constants import TEXT_SCROLL_DELAY, TEXT_SCROLL_SPEED


class StockRenderer(TickerRenderer):
    """
    Renderer for Stock objects

    Attributes:
        stocks (list):                              List of Stock objects
        ms_color (rgbmatrix.graphics.Color):        Market status color indicator
        symbol_x (int):                             Stock's symbol x-coord
        logo (PIL.Image):                           Stock's company logo image
    """

    def __init__(self, matrix, canvas, config, data):
        super().__init__(matrix, canvas, config, data)
        self.stocks = self.data.stocks
        self.ms_color = Color.RED if market_closed() else Color.GREEN
        self.symbol_x = self.coords['symbol']['x']
        self.logo = None

    def render(self):
        for stock in self.stocks:
            self.populate_data(stock)
            self.canvas.Clear()

            finished_scrolling = False
            if text_offscreen(self.name, self.canvas.width, self.primary_font.baseline - 1):
                time_started = time.time()
                first_run = True
                x = 1

                while not finished_scrolling:
                    self.canvas.Clear()

                    pos = self.render_name(x)
                    self.render_market_status()
                    self.render_symbol()
                    self.render_price()
                    self.render_percentage_change()
                    self.render_chart()

                    if first_run:
                        time.sleep(TEXT_SCROLL_DELAY)
                        first_run = False

                    time.sleep(TEXT_SCROLL_SPEED)

                    x = scroll_text(self.canvas.width, x, pos)

                    if time.time() - time_started >= self.config.rotation_rate:
                        finished_scrolling = True
            else:
                x = align_text(text=self.name,
                               x=Position.CENTER,
                               col_width=self.canvas.width,
                               font_width=self.secondary_font.baseline - 1)
                self.render_name(x)
                self.render_market_status()
                self.render_symbol()
                self.render_price()
                self.render_percentage_change()
                self.render_chart()

                time.sleep(self.config.rotation_rate)

            self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def populate_data(self, stock: Stock):
        """
        Populate attributes from Stock instance's attributes.
        :param stock: (data.Stock) Stock instance
        """
        super().populate_data(stock)
        self.logo = stock.logo

    def render_market_status(self):
        for x in range(2):
            DrawLine(self.canvas,
                     x, self.symbol_y,
                     x, self.symbol_y - self.secondary_font.height,
                     self.ms_color)

    def render_logo(self):
        x_offset, y_offset = align_image(self.logo,
                                         Position.CENTER,
                                         Position.BOTTOM,
                                         self.canvas.width,
                                         self.canvas.height)
        self.canvas.SetImage(self.logo, x_offset, y_offset)
