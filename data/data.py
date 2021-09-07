import time
import logging
import multitasking
from requests.exceptions import Timeout
import data.ticker
from constants import DATE_FORMAT
from utils import retry
from data.stock import Stock
from data.crypto import Crypto
from data.status import Status


class Data:
    """
    Data to be displayed on matrix

    Arguments:
        config (data.MatrixConfig):         MatrixConfig instance

    Attributes:
        time_format (str):                  Clock's time format
        date (str):                         Date string
        time (str):                         Time string
        tickers (list):                     List of Ticker instances
        status (data.Status):               Current update status
    """

    def __init__(self, config):
        self.config = config

        self.time_format = self.config.time_format
        self.date = None
        self.time = None
        self.tickers = []

        self.total_valid_tickers = len(self.config.stocks + self.config.cryptos)
        threads = min([self.total_valid_tickers, multitasking.cpu_count()*2])
        multitasking.set_max_threads(threads)
        self.updated_tickers = 0

        self.status = self.update()

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
            while len(self.tickers) < self.total_valid_tickers:
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
            if len(self.tickers) < 1:
                return self.initialize()
            else:
                logging.info('Checking for update...')
                self.updated_tickers = 0
                for ticker in self.tickers:
                    self.update_ticker(ticker)

                self.date = self.get_date()
                self.time = self.get_time()
                return Status.SUCCESS
        except Timeout:
            return Status.NETWORK_ERROR

    @multitasking.task
    def fetch_stock(self, stock: str, currency: str):
        """
        Fetch stock's data
        :param stock: (str) Stock ticker
        :param currency: (str) Stock's prices currency
        """
        instance = Stock(stock, currency)
        if instance.valid:
            self.tickers.append(instance)
        else:
            self.total_valid_tickers -= 1

    @multitasking.task
    def fetch_crypto(self, crypto: str, currency: str):
        """
        Fetch crypto's data
        :param crypto: (str) Crypto ticker
        :param currency: (str) Crypto's prices currency
        """
        instance = Crypto(crypto, currency)
        if instance.valid:
            self.tickers.append(instance)
        else:
            self.total_valid_tickers -= 1

    @multitasking.task
    def update_ticker(self, ticker: data.ticker.Ticker):
        """
        Update ticker's data
        :param ticker: (data.Ticker) Ticker instance to update
        """
        ticker.update()
        self.updated_tickers += 1

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
