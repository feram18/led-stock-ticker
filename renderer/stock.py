import time
from rgbmatrix.graphics import DrawText, DrawLine
from renderer.ticker import TickerRenderer
from data.stock import Stock
from utils import Color, market_closed, text_offscreen, scroll_text, Position, align_image, align_text
from constants import ROTATION_RATE, TEXT_SCROLL_DELAY, TEXT_SCROLL_SPEED


class StockRenderer(TickerRenderer):
    """
    Renderer for Stock objects

    Attributes:
        stocks (list):          List of Stock objects
        symbol_x (int):         Stock's symbol x-coord
        logo (PIL.Image):       Stock's company logo image
    """

    def __init__(self, matrix, canvas, config, data):
        super().__init__(matrix, canvas, config, data)
        self.stocks = self.data.stocks
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

                    # Render elements
                    self.render_chart()
                    pos = self.render_name(x)
                    self.render_market_status()
                    self.render_symbol()
                    self.render_price()
                    self.render_percentage_change()

                    if first_run:
                        time.sleep(TEXT_SCROLL_DELAY)
                        first_run = False

                    time.sleep(TEXT_SCROLL_SPEED)

                    x = scroll_text(self.canvas.width, x, pos)

                    if time.time() - time_started >= ROTATION_RATE:
                        finished_scrolling = True
            else:
                # Render elements
                self.render_chart()
                x = align_text(text=self.name,
                               x=Position.CENTER,
                               col_width=self.canvas.width,
                               font_width=self.secondary_font.baseline - 1)
                self.render_name(x)
                self.render_market_status()
                self.render_symbol()
                self.render_price()
                self.render_percentage_change()

                time.sleep(ROTATION_RATE)

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
                     Color.RED if market_closed() else Color.GREEN)

    def render_logo(self):
        x_offset, y_offset = align_image(self.logo,
                                         Position.CENTER,
                                         Position.BOTTOM,
                                         self.canvas.width,
                                         self.canvas.height)
        self.canvas.SetImage(self.logo, x_offset, y_offset)
