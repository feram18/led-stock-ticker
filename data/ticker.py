import logging
import time
import yfinance as yf
from requests.exceptions import Timeout
from constants import UPDATE_RATE
from utils import convert_currency
from data.status import Status


class Ticker:
    """
        Class to represent a Ticker object

        Arguments:
            ticker (str):                       Ticker string
            currency (str):                     Currency prices will be displayed on

        Attributes:
            data (yfinance.Ticker):             yfinance Ticker instance
            name (str):                         Ticker's full name
            prev_close_price (float):           Ticker's previous day's close price
            current_price (float):              Ticker's current price
            value_change (float):               Ticker's value change since previous day's close price
            pct_change (str):                   Ticker's value percentage change since previous day's close price
            chart_prices (list):                List of close prices over the past two days
            valid (bool):                       Indicates if ticker is valid
            initialized (bool):                 Indicates if data has been initialized
            last_updated (float):               Time Ticker's data was last updated
            update_status (data.Status):        Indicates update status.
        """
    def __init__(self, ticker: str, currency: str):
        self.data = None
        self.ticker = ticker
        self.name = None
        self.current_price = None
        self.prev_close_price = None
        self.value_change = None
        self.pct_change = None
        self.chart_prices = None
        self.valid = True  # Assume true until determined otherwise
        self.currency = currency

        self.initialized = False
        self.update_status = self.update()  # Force an initial update
        self.last_updated = time.time()

    def initialize(self) -> Status:
        """
        Setup ticker's initial data.
        :return status: (data.Status) Update status
        :exception KeyError: If incorrect data type is provided as an argument. Can occur when a ticker is not valid.
        :exception Timeout: If the request timed out
        """
        logging.debug(f'Fetching initial data for {self.ticker}.')

        try:
            self.data = yf.Ticker(self.ticker)

            self.name = self.get_name()
            self.current_price = self.get_current_price()
            self.prev_close_price = self.get_previous_close_price()
            self.value_change = self.get_value_change()
            self.pct_change = self.get_percentage_change()
            self.chart_prices = self.get_chart_prices()

            self.last_updated = time.time()
            self.initialized = True
            return Status.SUCCESS
        except KeyError:
            logging.error(f'No data available for {self.ticker}.')
            self.valid = False
            return Status.FAIL
        except Timeout:
            return Status.NETWORK_ERROR

    def update(self, force: bool = False) -> Status:
        """
        Update only the data that may have changed since last update
        i.e. Exclude the ticker's name, previous day close price, and logo image.
        :param force: (bool default=False) Force update
        :return status: (data.Status) Update status
        :exception Timeout: If the request timed out
        """
        if not self.initialized:
            return self.initialize()
        elif force or self.should_update():
            logging.debug(f'Fetching new data for {self.ticker}.')
            try:
                self.data = yf.Ticker(self.ticker)
                self.current_price = self.get_current_price()
                self.value_change = self.get_value_change()
                self.pct_change = self.get_percentage_change()
                self.chart_prices = self.get_chart_prices()

                self.last_updated = time.time()
                return Status.SUCCESS
            except Timeout:
                return Status.NETWORK_ERROR

    def get_name(self) -> str:
        """
        Fetch ticker's full name. i.e. TSLA -> Tesla Inc.
        :return: name: (str) Name
        :exception KeyError: If incorrect data type is provided as an argument. Can occur when a ticker is not valid.
        """
        try:
            return self.data.info['shortName']
        except KeyError:
            self.valid = False
            self.update_status = Status.FAIL
            return ''

    def get_current_price(self) -> float:
        """
        Fetch the ticker's price at the current time.
        If currency is not set to USD, convert value to user-selected currency.
        :return: current_price: (float) Current price
        :exception KeyError: If incorrect data type is provided as an argument. Can occur when a ticker is not valid.
        """
        try:
            current_price = self.data.info["regularMarketPrice"]
            if self.currency != 'USD':
                current_price = convert_currency('USD', self.currency, current_price)
            return float(f'{current_price:.2f}')
        except KeyError:
            self.valid = False
            self.update_status = Status.FAIL
            return 0.00

    def get_previous_close_price(self) -> float:
        """
        Fetch the ticker's previous day's close price.
        If currency is not set to USD, convert value to user-selected currency.
        :return: prev_close_price: (float) Previous day's close price
        :exception KeyError: If incorrect data type is provided as an argument. Can occur when a ticker is not valid.
        """
        try:
            prev_close_price = self.data.info['regularMarketPreviousClose']
            if self.currency != 'USD':
                prev_close_price = convert_currency('USD', self.currency, prev_close_price)
            return prev_close_price
        except KeyError:
            self.valid = False
            self.update_status = Status.FAIL
            return 0.00

    def get_value_change(self) -> float:
        """
        Calculate the ticker's price value change since previous day's close price.
        :return: value_change: (str) Value change
        """
        return float(f'{self.current_price - self.prev_close_price:.2f}')

    def get_percentage_change(self) -> str:
        """
        Calculate the ticker's percentage change since previous day's close price.
        :return: pct_change: (str) Percentage change
        :exception ZeroDivisionError: If previous day's close price is zero.
        """
        try:
            return f'{100 * (self.value_change/abs(self.prev_close_price)):.2f}%'
        except ZeroDivisionError:
            self.valid = False
            return '0.00%'

    def get_chart_prices(self) -> list:
        """
        Fetch historical market data for chart.
        :return: chart_prices: (list) List of historical prices
        """
        chart_prices = self.data.history(interval='1m', period='1d')['Close'].tolist()
        if len(chart_prices) < 100:
            chart_prices = self.data.history(interval='1m', period='2d')['Close'].tolist()
        elif not chart_prices:
            self.valid = False
            self.update_status = Status.FAIL
            chart_prices.append(0.00)
        return chart_prices

    def should_update(self) -> bool:
        """
        Returns Boolean value to determine if the ticker's data should be updated.
        i.e. If 2 minutes have passed since data was last fetched, an update is needed.
        Update rate depends on number of tickers selected by user.
        :return: should_update: (bool)
        """
        current_time = time.time()
        time_delta = current_time - self.last_updated
        return time_delta >= UPDATE_RATE

    def __str__(self):
        return f'<{self.__class__.__name__} {hex(id(self))}> ' \
               f'Ticker: {self.ticker}; ' \
               f'Full Name: {self.name}; ' \
               f'Previous Day Close Price: {self.prev_close_price}; ' \
               f'Current Price: {self.current_price}; ' \
               f'Value Change: {self.value_change}; ' \
               f'Percentage Change: {self.pct_change}'
