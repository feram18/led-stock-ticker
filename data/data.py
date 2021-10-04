import time
import logging
import multitasking
from requests.exceptions import Timeout
from constants import DATE_FORMAT, UPDATE_RATE
from utils import retry
from data.crypto import Crypto
from data.stock import Stock
from data.ticker import Ticker
from data.status import Status


class Data:
    """
    Data to be displayed on matrix

    Arguments:
        matrix_config (config.MatrixConfig):        MatrixConfig instance

    Attributes:
        time_format (str):                          Clock's time format
        date (str):                                 Date string
        time (str):                                 Time string
        stocks (list):                              List of Stock instances
        cryptos (list):                             List of Crypto instances
        total_valid_tickers (int):                  Total number of valid tickers
        status (data.Status):                       Current update status
    """

    def __init__(self, matrix_config):
        self.config = matrix_config

        self.time_format = self.config.time_format
        self.date = None
        self.time = None
        self.stocks = []
        self.cryptos = []

        self.total_valid_tickers = len(self.config.stocks + self.config.cryptos)
        threads = min([self.total_valid_tickers, multitasking.cpu_count()*2])
        multitasking.set_max_threads(threads)

        self.status = self.update()
        self.last_updated = time.time()

    def initialize(self) -> Status:
        """
        Initialize Ticker instances, and append those which are valid to tickers list.
        :return: status: (data.Status) Update status
        :exception Timeout: If the request timed out
        """
        try:
            logging.info('Initializing data...')

            for stock in self.config.stocks:  # Initialize stocks
                self.fetch_stock(stock, self.config.currency)
            for crypto in self.config.cryptos:  # Initialize cryptos
                self.fetch_crypto(crypto, self.config.currency)
            # Wait until all tickers are initialized
            while len(self.stocks + self.cryptos) < self.total_valid_tickers:
                time.sleep(0.1)

            self.date = self.get_date()
            self.time = self.get_time()
            return Status.SUCCESS
        except Timeout:
            retry(self.initialize())

    def update(self) -> Status:
        """
        Update tickers' prices, date, and time.
        :return: status: (data.Status) Update status
        :exception Timeout: If the request timed out
        """
        try:
            if len(self.stocks + self.cryptos) < 1:
                return self.initialize()
            else:
                logging.info('Checking for update...')
                for ticker in self.stocks + self.cryptos:
                    self.update_ticker(ticker)

                self.last_updated = time.time()

                return Status.SUCCESS
        except Timeout:
            return Status.NETWORK_ERROR

    def update_clock(self):
        """Update date & time"""
        self.date = self.get_date()
        self.time = self.get_time()

    @multitasking.task
    def fetch_stock(self, stock: str, currency: str):
        """
        Fetch stock's data
        :param stock: (str) Stock ticker
        :param currency: (str) Stock's prices currency
        """
        ticker = Stock(stock, currency)
        if ticker.valid:
            self.stocks.append(ticker)
        else:
            self.total_valid_tickers -= 1

    @multitasking.task
    def fetch_crypto(self, crypto: str, currency: str):
        """
        Fetch crypto's data
        :param crypto: (str) Crypto ticker
        :param currency: (str) Crypto's prices currency
        """
        ticker = Crypto(crypto, currency)
        if ticker.valid:
            self.cryptos.append(ticker)
        else:
            self.total_valid_tickers -= 1

    @multitasking.task
    def update_ticker(self, ticker: Ticker):
        """
        Update ticker's data
        :param ticker: (data.Ticker) Ticker object to update
        """
        ticker.update()

    def get_time(self) -> str:
        """
        Get current time as a string.
        :return: time: (str) Current time
        """
        return time.strftime(self.time_format)

    @staticmethod
    def get_date() -> str:
        """
        Get current date as a string.
        :return: date: (str) Current date
        """
        return time.strftime(DATE_FORMAT)

    def should_update(self) -> bool:
        """
        Returns Boolean value to determine if tickers should be updated.
        i.e. If 10 minutes have passed since data was last fetched, an update is needed.
        :return: should_update: (bool)
        """
        current_time = time.time()
        time_delta = current_time - self.last_updated
        return time_delta >= UPDATE_RATE
