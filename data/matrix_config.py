from utils import read_json
import debug

CONFIG_FILE = "config.json"
COLORS_FILE = "colors.json"
DEFAULT_SYMBOLS = ["TSLA", "AMZN", "AAPL", "MSFT"]
DEFAULT_COUNTRY = "US"
DEFAULT_CURRENCY = "USD"
DEFAULT_TIMEZONE = "EST"
DEFAULT_TIME_FORMAT = "12h"
LAYOUT_DIR = "layout/"


class MatrixConfig:
    def __init__(self, width, height):
        self.config = self.load_config()

        # Matrix dimensions
        self.width = width
        self.height = height

        # Layout configuration
        self.layout = self.load_layout()

        # Color configuration
        self.colors = self.load_colors()

        # Twelve Data API key
        self.api_key = self.config["api_key"]

        # User's preferred symbols
        self.symbols = self.config["symbols"]

        # Miscellaneous configuration options
        self.country = self.config["country"]
        self.currency = self.config["currency"]
        self.timezone = self.config["timezone"]
        self.time_format = self.config["time_format"]
        self.debug = self.config["debug"]

        # Check options validity or set default values
        self.check_country()
        self.check_currency()
        self.check_timezone()
        self.check_time_format()
        self.check_debug()

    def load_config(self):
        config = read_json(CONFIG_FILE)
        return config

    def load_layout(self):
        layout = LAYOUT_DIR + "w{}h{}.json".format(self.width, self.height)
        return read_json(layout)

    def load_colors(self):
        colors = read_json(COLORS_FILE)
        return colors

    def check_preferred_symbols(self):
        if not isinstance(self.preferred_symbols, str) and not isinstance(self.preferred_symbols, list):
            debug.warning("Symbols should be an array of symbols or a single symbol string."
                          "Using default preferred_symbols, {}".format(DEFAULT_SYMBOLS))
            self.preferred_symbols = DEFAULT_SYMBOLS

        if isinstance(self.preferred_symbols, str):
            symbol = self.preferred_symbols
            self.preferred_symbols = [symbol]

    def check_country(self):
        if self.country is None or not isinstance(self.country, str):
            self.country = DEFAULT_COUNTRY

    def check_currency(self):
        if self.currency is None or not isinstance(self.currency, str):
            self.currency = DEFAULT_CURRENCY

    def check_timezone(self):
        if self.timezone is None or not isinstance(self.currency, str):
            self.timezone = DEFAULT_TIMEZONE

    def check_time_format(self):
        if self.time_format is None or self.time_format.lower() != ("12h" or "24h"):
            self.time_format = DEFAULT_TIME_FORMAT

    def check_debug(self):
        if not isinstance(self.debug, bool):
            self.debug = True
