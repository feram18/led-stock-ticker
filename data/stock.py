from requests import RequestException
from datetime import datetime
from pytz import timezone
import requests
import debug
import time
import sys

BASE_URL = "https://api.twelvedata.com/"
DECIMAL_PLACES = 2
OUTPUT_SIZE = 1
INTERVAL = "1day"
EMPTY_STRING = ""
UPDATE_RATE = 90.0  # 1m30s


class Stock:
    def __init__(self, api_key, symbol, country):
        self.api_key = api_key

        self.country = country

        self.symbol = symbol
        self.name = None
        self.prev_day_close_price = None
        self.current_price = None
        self.value_change = None
        self.percentage_change = None

        # Check for validity
        self.symbol_valid = self.symbol_valid()
        self.api_key_valid = self.api_key_valid()

        self.data_initialized = False
        self.last_updated = time.time()

        # Force an initial update
        self.update_data()

    # Setup initial data to be displayed
    def setup_data(self):
        debug.log("Fetching initial data...")
        self.name = self.get_symbol_name()
        self.prev_day_close_price = self.get_previous_day_close_price()
        self.current_price = self.get_current_price()
        self.value_change = self.get_value_change()
        self.percentage_change = self.get_percentage_change()

    # Only update data that may have changed since last update
    # i.e. exclude the stock/cryptocurrency's full name and previous day close price
    def update_data(self, force=False):
        if self.data_initialized is False:
            self.setup_data()
            self.data_initialized = True

        if force is True or self.should_update():
            debug.log("Fetching new data...")
            self.last_updated = time.time()

            self.current_price = self.get_current_price()
            self.value_change = self.get_value_change()
            self.percentage_change = self.get_percentage_change()

    # Fetch the previous day's close price.
    # To be used in percentage and value change calculations
    def get_previous_day_close_price(self):
        debug.log("Fetching previous day' close price for {}".format(self.symbol))
        url = BASE_URL + "/time_series?symbol={}&interval={}&outputsize={}&dp={}&previous_close={}&apikey={}" \
            .format(self.symbol,
                    INTERVAL,
                    OUTPUT_SIZE,
                    DECIMAL_PLACES,
                    True,
                    self.api_key)
        try:
            response = requests.get(url).json()
            close_price = float(response["values"][0]["previous_close"])
            return close_price
        except RequestException as e:
            debug.error("Unable to fetch previous day' close price for {}".format(self.symbol))
            debug.error(e)

    # Fetch the stock/cryptocurrency's price at the current time
    def get_current_price(self):
        debug.log("Fetching current price for {}".format(self.symbol))
        url = BASE_URL + "/price?symbol={}&dp={}&apikey={}".format(self.symbol, DECIMAL_PLACES, self.api_key)
        try:
            response = requests.get(url).json()
            price = float(response["price"])
            return price
        except RequestException as e:
            debug.error("Unable to fetch current price for {}".format(self.symbol))
            debug.error(e)

    # Calculate the value change since previous day's close price
    def get_value_change(self):
        debug.log("Calculating value change")
        result = "{:.2f}".format(self.current_price - self.prev_day_close_price)
        return result

    # Calculate the percentage change since previous day's close price
    def get_percentage_change(self):
        debug.log("Calculating percentage change")
        result = str("{:.2f}".format(
            100 * ((self.current_price - self.prev_day_close_price) / abs(self.prev_day_close_price)))) + "%"
        return result

    # Fetch stock's full name.
    # i.e. TSLA -> Tesla Inc.
    def get_symbol_name(self):
        debug.log("Fetching name for {}".format(self.symbol))
        url = BASE_URL + "/stocks?symbol={}&country={}".format(self.symbol, self.country)
        try:
            response = requests.get(url).json()
            if len(response["data"]) > 0:
                return response["data"][0]["name"]
            else:
                debug.log("Checking if {} is a cryptocurrency".format(self.symbol))
                return self.get_crypto_name()
        except RequestException as e:
            debug.error("Failed to fetch name for {}".format(self.symbol))
            debug.error(e)

    # Fetch cryptocurrency's full name.
    # i.e. BTC -> Bitcoin
    def get_crypto_name(self):
        debug.log("Fetching name for {}".format(self.symbol))
        url = BASE_URL + "/cryptocurrencies?symbol={}".format(self.symbol)
        try:
            response = requests.get(url).json()
            full_name = response["data"][0]["currency_base"]
            return full_name
        except RequestException as e:
            debug.error("Failed to fetch name for {}".format(self.symbol))
            debug.error(e)

    # Verify if symbol is valid
    def symbol_valid(self):
        debug.log("Verifying validity of symbol: {}".format(self.symbol))
        url = BASE_URL + "/symbol_search?symbol={}".format(self.symbol)
        try:
            response = requests.get(url).json()
            if response["data"][0]["symbol"] == self.symbol:
                return True
            else:
                debug.error("Symbol: {} does not exist.".format(self.symbol))
                sys.exit(1)
        except RequestException as e:
            debug.error("Failed to verify validity of symbol: {}".format(self.symbol))
            debug.error(e)

    # Verify if API key is valid
    def api_key_valid(self):
        if self.api_key is None or len(self.api_key) < 32:
            debug.error("API key is not valid. Please verify your config.json file.")
            debug.error("If you do not have an API key, you can get a free key at twelvedata.com/register")
            sys.exit(1)
        else:
            return True

    # Returns Boolean value to determine if the stock's data should be updated.
    # i.e. If 90 seconds have passed since data was last fetched, update is needed
    def should_update(self):
        if not self.weekend() and not self.after_hours():
            current_time = time.time()
            time_delta = current_time - self.last_updated
            return time_delta >= UPDATE_RATE
        else:
            return False

    # Check if current time is not between 09:30 AM and 04:00 PM EST range (Regular stock market hours)
    def after_hours(self):
        current_time = datetime.now(timezone("US/Eastern"))  # Current time in EST
        openMarket = current_time.replace(hour=9, minute=30, second=0, microsecond=0)   # 09:30 AM EST
        closeMarket = current_time.replace(hour=16, minute=0, second=0, microsecond=0)  # 04:00 PM EST
        return current_time < openMarket or current_time > closeMarket

    # Check if it is a weekend
    def weekend(self):
        week_day_no = datetime.today().weekday()
        return week_day_no > 5  # 5 Sat, 6 Sun

    def __str__(self):
        return "<{} {}> Symbol: {}; " \
                "Full Name: {}; " \
                "Previous Day Close Price: {}; " \
                "Current Price: {}; " \
                "Value Change: {}; " \
                "Percentage Change: {}".format(self.__class__.__name__,
                                               hex(id(self)),
                                               self.symbol,
                                               self.name,
                                               self.prev_day_close_price,
                                               self.current_price,
                                               self.value_change,
                                               self.percentage_change)
