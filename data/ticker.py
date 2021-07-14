from requests import RequestException
from datetime import datetime
from pytz import timezone
import constants
import requests
import logging
import time
import sys


class Ticker:
    """
    Class to represent a Ticker object

    Properties:
        api_key         String containing TwelveData API key
        ticker          Ticker string
        country         Country string
        update_rate     Float value of update frequency (in seconds)
    """
    def __init__(self, api_key: str, ticker: str, country: str, update_rate: float):
        self.api_key = api_key

        self.update_rate = update_rate
        self.country = country

        self.ticker = ticker
        self.name = None
        self.prev_day_close_price = None
        self.current_price = None
        self.value_change = None
        self.percentage_change = None

        # Check for tickers' validity
        self.ticker_valid = self.ticker_valid()

        self.data_initialized = False
        self.last_updated = time.time()

        # Force an initial update
        self.update_data()

    def setup_data(self):
        """
        Setup initial data
        """
        logging.debug("Fetching initial data...")

        self.name = self.get_stock_name()
        self.prev_day_close_price = self.get_previous_day_close_price()
        self.current_price = self.get_current_price()
        self.value_change = self.get_value_change()
        self.percentage_change = self.get_percentage_change()

    def update_data(self, force=False):
        """
        Only update data that may have changed since last update
        i.e. Exclude the stock/cryptocurrency's full name and previous day close price
        :param force: boolean (default False)
        """
        if self.data_initialized is False:
            self.setup_data()
            self.data_initialized = True

        if force is True or self.should_update():
            logging.debug("Fetching new data...")

            self.last_updated = time.time()

            self.current_price = self.get_current_price()
            self.value_change = self.get_value_change()
            self.percentage_change = self.get_percentage_change()

    def get_previous_day_close_price(self) -> float:
        """
        Fetch the ticker's previous day's close price. To be used in percentage and value change calculations.
        :return: close_price: float
        """
        logging.debug(f"Fetching previous day' close price for {self.ticker}")

        url = constants.PREVIOUS_DAY_CLOSE_PRICE_URL.format(self.ticker,
                                                            constants.INTERVAL,
                                                            constants.OUTPUT_SIZE,
                                                            constants.DECIMAL_PLACES,
                                                            True,
                                                            self.api_key)
        try:
            response = requests.get(url).json()
            close_price = float(response["values"][0]["previous_close"])
            return close_price
        except RequestException:
            logging.error(f"Unable to fetch previous day' close price for {self.ticker}")

    def get_current_price(self) -> float:
        """
        Fetch the ticker's price at the current time.
        :return: price: float
        """
        logging.debug(f"Fetching current price for {self.ticker}")

        url = constants.CURRENT_PRICE_URL.format(self.ticker, constants.DECIMAL_PLACES, self.api_key)

        try:
            response = requests.get(url).json()
            price = float(response["price"])
            return price
        except RequestException:
            logging.error(f"Unable to fetch current price for {self.ticker}")

    def get_value_change(self) -> str:
        """
        Calculate the ticker's price value change since previous day's close price.
        :return: value_change: str
        """
        logging.debug("Calculating value change")

        value_change = "{:.2f}".format(self.current_price - self.prev_day_close_price)
        return value_change

    def get_percentage_change(self) -> str:
        """
        Calculate the ticker's percentage change since previous day's close price.
        :return: pct_change: str
        """
        logging.debug("Calculating percentage change")

        pct_change = "{:.2f}".format(100 * ((self.current_price - self.prev_day_close_price) /
                                            abs(self.prev_day_close_price))) + "%"
        return pct_change

    def get_stock_name(self) -> str:
        """
        Fetch stock's full name. i.e. TSLA -> Tesla Inc.
        :return: name: str
        """
        logging.debug(f"Fetching name for {self.ticker}")

        url = constants.STOCK_NAME_URL.format(self.ticker, self.country)

        try:
            response = requests.get(url).json()
            if len(response["data"]) > 0:
                return response["data"][0]["name"]
            else:
                logging.debug(f"Checking if {self.ticker} is a cryptocurrency")
                return self.get_crypto_name()
        except RequestException:
            logging.error(f"Failed to fetch name for {self.ticker}")

    def get_crypto_name(self) -> str:
        """
        Fetch cryptocurrency's full name. i.e. BTC -> Bitcoin.
        :return: name: str
        """
        logging.debug(f"Fetching name for {self.ticker}")

        url = constants.CRYPTO_NAME_URL.format(self.ticker)

        try:
            response = requests.get(url).json()
            full_name = response["data"][0]["currency_base"]
            return full_name
        except RequestException:
            logging.error(f"Failed to fetch name for {self.ticker}")

    def ticker_valid(self) -> bool:
        """
        Verify ticker's validity.
        :return:
        """
        logging.debug(f"Verifying validity of ticker: {self.ticker}")

        url = constants.SYMBOL_SEARCH_URL.format(self.ticker)

        try:
            response = requests.get(url).json()
            if response["data"][0]["symbol"] == self.ticker:
                return True
            else:
                logging.error(f"Ticker: {self.ticker} does not exist.")
                sys.exit(1)
        except RequestException:
            logging.error(f"Failed to verify validity of ticker: {self.ticker}")

    def should_update(self) -> bool:
        """
        Returns Boolean value to determine if the stock's data should be updated.
        i.e. If 2 minutes (120 seconds) have passed since data was last fetched, update is needed.
        :return: should_update: bool
        """
        if not self.weekend() and not self.after_hours():
            current_time = time.time()
            time_delta = current_time - self.last_updated
            return time_delta >= self.update_rate
        else:
            return False

    @staticmethod
    def after_hours() -> bool:
        """
        Determine if current time is not between 09:30 AM and 04:00 PM EST range (Regular stock market hours).
        :return: after_hours: bool
        """
        current_time = datetime.now(timezone(constants.EASTERN_TZ))  # Current time in EST
        open_market = current_time.replace(hour=9, minute=30, second=0, microsecond=0)  # 09:30 AM EST
        close_market = current_time.replace(hour=16, minute=0, second=0, microsecond=0)  # 04:00 PM EST
        return current_time < open_market or current_time > close_market

    @staticmethod
    def weekend() -> bool:
        """
        Determine if today is a weekend day
        :return: weekend: bool
        """
        week_day_no = datetime.today().weekday()
        return week_day_no > 5  # 5 Sat, 6 Sun

    def __str__(self):
        return f"<{self.__class__.__name__} {hex(id(self))}> " \
               f"Ticker: {self.ticker}; " \
               f"Full Name: {self.name}; " \
               f"Previous Day Close Price: {self.prev_day_close_price}; " \
               f"Current Price: {self.current_price}; " \
               f"Value Change: {self.value_change}; " \
               f"Percentage Change: {self.percentage_change}"
