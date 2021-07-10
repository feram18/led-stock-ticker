from utils import read_json
import constants
import logging
import sys


class Config:
    logging.basicConfig(filename='led-stock-ticker.log',
                        filemode='w',
                        format='%(asctime)s:%(levelname)s:%(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.DEBUG)

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

        # User's preferred tickers
        self.tickers = self.config["tickers"]

        # Miscellaneous configuration options
        self.country = self.config["country"]
        self.currency = self.config["currency"]
        self.timezone = self.config["timezone"]
        self.time_format = self.config["time_format"]

        # Check options validity or set default values
        self.check_country()
        self.check_currency()
        self.check_timezone()
        self.check_time_format()

    def load_config(self):
        """
        Load configuration file
        :return: config: JSON
        """
        try:
            config = read_json(constants.CONFIG_FILE)
            return config
        except FileNotFoundError:
            logging.error("Config file not found. Make sure you have a config.json file setup.")
            sys.exit(1)

    def load_layout(self):
        """
        Load layout configuration file
        :return: layout: JSON
        """
        try:
            layout = constants.LAYOUT_FILE.format(self.width, self.height)
            return read_json(layout)
        except FileNotFoundError:
            logging.error(f"w{self.width}h{self.height}.json file does not exist.")
            sys.exit(1)

    def load_colors(self):
        """
        Load colors configuration file
        :return: colors: JSON
        """
        try:
            colors = read_json(constants.COLORS_FILE)
            return colors
        except FileNotFoundError:
            logging.error(f"{constants.COLORS_FILE} does not exist.")
            sys.exit(1)

    def check_preferred_tickers(self):
        """
        Determine if tickers on config are an instance of a list (several tickers) or a single instance of a string
        (i.e. One ticker). Else, set tickers list to default values (TSLA, AMZN, AAPL, MSFT).
        """
        if not isinstance(self.tickers, str) and not isinstance(self.tickers, list):
            logging.warning(f"Symbols should be an array of tickers or a single ticker string."
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
