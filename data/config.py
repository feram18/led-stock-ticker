from utils import read_json
import constants
import logging
import sys


class Config:
    # Set Log file configuration
    logging.basicConfig(filename='led-stock-ticker.log',
                        filemode='w',
                        format='%(asctime)s:%(levelname)s:%(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.DEBUG)

    def __init__(self, width: int, height: int):
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

        # User's preferred tickers
        self.tickers = self.config["tickers"]

        # Miscellaneous configuration options
        self.country = self.config["country"]
        self.currency = self.config["currency"]
        self.timezone = self.config["timezone"]
        self.time_format = self.config["time_format"]

        # Check options validity or set default values
        self.check_apikey()
        self.check_tickers()
        self.check_country()
        self.check_currency()
        self.check_timezone()
        self.check_time_format()

    def load_config(self) -> dict:
        """
        Load configuration file
        :return: config: dict
        """
        try:
            config = read_json(constants.CONFIG_FILE)
            return config
        except FileNotFoundError:
            logging.error("Config.json file not found.")
            sys.exit(1)

    def load_layout(self) -> dict:
        """
        Load layout configuration file
        :return: layout: dict
        """
        try:
            layout = constants.LAYOUT_FILE.format(self.width, self.height)
            return read_json(layout)
        except FileNotFoundError:
            logging.error(f"w{self.width}h{self.height}.json file does not exist.")
            sys.exit(1)

    def load_colors(self) -> dict:
        """
        Load colors configuration file
        :return: colors: dict
        """
        try:
            colors = read_json(constants.COLORS_FILE)
            return colors
        except FileNotFoundError:
            logging.error(f"{constants.COLORS_FILE} does not exist.")
            sys.exit(1)

    def check_apikey(self):
        """
        Verify if TwelveData API key is valid.
        """
        if self.api_key is None or len(self.api_key) < 32:
            logging.error(f"API key {self.api_key} is not valid")
            print("Invalid API key. Check your config.json file."
                  "If you do not have an API key, you can get a free one at twelvedata.com/register")
            sys.exit(1)

    def check_tickers(self):
        """
        Determine if tickers on config are an instance of a list (several tickers) or a single instance of a string
        (i.e. One ticker). Else, set tickers list to default values (TSLA, AMZN, AAPL, MSFT).
        """
        if not isinstance(self.tickers, str) and not isinstance(self.tickers, list):
            logging.warning("Symbols should be an array of tickers or a single ticker string."
                            "Using default preferred_tickers, {}".format(constants.DEFAULT_TICKERS))
            self.tickers = constants.DEFAULT_TICKERS

        if isinstance(self.tickers, str):
            ticker = self.tickers
            self.tickers = [ticker]

    def check_country(self):
        """
        Determine if country is an instance of a string. Else, set to default value (US).
        """
        if self.country is None or not isinstance(self.country, str):
            self.country = constants.DEFAULT_COUNTRY

    def check_currency(self):
        """
        Determine if currency value is an instance of a string. Else, set to default value (USD).
        """
        if self.currency is None or not isinstance(self.currency, str):
            self.currency = constants.DEFAULT_CURRENCY

    def check_timezone(self):
        """
        Determine if timezone value is an instance of a string. Else, set to default value (EST).
        """
        if self.timezone is None or not isinstance(self.timezone, str):
            self.timezone = constants.DEFAULT_TIMEZONE

    def check_time_format(self):
        """
        Determine if time format is an accepted value (12h or 24h). Else, set to default value (12h).
        """
        if self.time_format is None or self.time_format.lower() != ("12h" or "24h"):
            self.time_format = constants.DEFAULT_TIME_FORMAT
