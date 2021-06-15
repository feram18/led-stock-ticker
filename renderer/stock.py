from rgbmatrix import graphics
import utils as u
import time

ROTATION_RATE = 15.0  # In seconds
SCROLL_SPEED = 0.1


class StockRenderer:
    def __init__(self, matrix, canvas, data):
        self.matrix = matrix
        self.canvas = canvas

        # Load coords
        self.coords = data.config.layout["coords"]["stock"]

        # Load colors
        self.colors = data.config.colors["stock"]
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
        self.symbols = data.symbols

        self.currency = data.config.currency

        self.name = None
        self.name_y = None

        self.symbol_ = None
        self.symbol_x = None
        self.symbol_y = None

        self.price = None
        self.price_x = None
        self.price_y = None

        self.value_and_pct_change = None
        self.value_x = None
        self.value_y = None

        self.value_indicator_color = None

        self.finished_scrolling = False

    def render(self):
        for symbol in self.symbols:
            self.set_data(symbol)

            self.canvas.Clear()

            if u.text_offscreen(self.name, self.canvas.width, self.FONT_TOM_THUMB["width"]):
                time_started = time.time()
                name_x = 1

                while self.finished_scrolling is False:
                    self.canvas.Clear()

                    # Render elements
                    pos = self.__render_full_name(name_x)
                    self.__render_symbol()
                    self.__render_price()
                    self.__render_value_and_pct_change()

                    time.sleep(SCROLL_SPEED)

                    name_x = self.__update_text_position(name_x, pos)

                    if time.time() - time_started >= ROTATION_RATE:
                        self.finished_scrolling = True
            else:
                name_x = u.align_center(self.name, (self.canvas.width / 2), self.FONT_TOM_THUMB["width"])

                # Render elements
                self.__render_full_name(name_x)
                self.__render_symbol()
                self.__render_price()
                self.__render_value_and_pct_change()

                time.sleep(ROTATION_RATE)

            self.finished_scrolling = False
            self.canvas = self.matrix.SwapOnVSync(self.canvas)

    # Set Stock/Cryptocurrency data
    def set_data(self, symbol):
        self.name = symbol.name
        self.name_y = self.coords["name"]["y"]

        self.symbol_ = self.format_symbol(symbol.symbol)
        self.symbol_x = self.coords["symbol"]["x"]
        self.symbol_y = self.coords["symbol"]["y"]

        self.price = "${}".format(symbol.current_price)
        self.price_x = u.align_right(self.price, self.canvas.width, self.FONT_TOM_THUMB["width"])
        self.price_y = self.coords["price"]["y"]

        self.value_and_pct_change = "{} {}".format(symbol.value_change, symbol.percentage_change)
        self.value_x = u.align_center(self.value_and_pct_change, (self.canvas.width/2), self.FONT_TOM_THUMB["width"])
        self.value_y = self.coords["value_and_pct_change"]["y"]

        self.value_indicator_color = self.set_indicator_color(float(symbol.value_change))

    def __render_full_name(self, name_x):
        return graphics.DrawText(self.canvas,
                                 self.primary_font,
                                 name_x,
                                 self.name_y,
                                 self.main_color,
                                 self.name)

    def __render_symbol(self):
        graphics.DrawText(self.canvas, self.large_font, self.symbol_x, self.symbol_y, self.main_color, self.symbol_)

    def __render_price(self):
        graphics.DrawText(self.canvas, self.primary_font, self.price_x, self.price_y, self.main_color, self.price)

    def __render_value_and_pct_change(self):
        graphics.DrawText(self.canvas,
                          self.primary_font,
                          self.value_x,
                          self.value_y,
                          self.value_indicator_color,
                          self.value_and_pct_change)

    # Update x-coord on scrolling text
    def __update_text_position(self, full_name_x, pos):
        if full_name_x + pos < 1:
            return self.canvas.width
        else:
            return full_name_x - 1

    # Format cryptocurrency to remove currency value from it.
    # i.e. BTC/USD -> BTC
    def format_symbol(self, symbol):
        currency_postfix = "/{}".format(self.currency)
        if currency_postfix.upper() in symbol:
            return symbol.replace(currency_postfix, "")
        else:
            return symbol

    # Determines if value has decreased and returns appropriate color
    def set_indicator_color(self, value_change):
        if value_change < 0:  # Value has decreased
            return u.load_color(self.colors["decrease"])  # Red
        else:  # Value has increased
            return u.load_color(self.colors["increase"])  # Green
