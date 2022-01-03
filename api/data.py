import time
import logging
import multitasking
from dataclasses import dataclass, field
from typing import List
from config.matrix_config import MatrixConfig
from data.crypto import Crypto
from data.stock import Stock
from data.ticker import Ticker
from data.status import Status
from constants import DATE_FORMAT, UPDATE_RATE


@dataclass
class Data:
    config: MatrixConfig
    date: str = field(init=False)
    time: str = field(init=False)
    time_format: str = field(init=False)
    cryptos: List[Ticker] = field(default_factory=list)
    stocks: List[Ticker] = field(default_factory=list)
    valid_tickers: int = 0
    status: Status = Status.SUCCESS
    last_updated: float = None

    def __post_init__(self):
        self.time_format = self.config.time_format
        self.valid_tickers = len(self.config.stocks + self.config.cryptos)
        self.last_updated = time.time()

        threads = min([self.valid_tickers, multitasking.cpu_count() * 2])
        multitasking.set_max_threads(threads)

        self.initialize()

    def initialize(self) -> Status:
        """
        Initialize Ticker instances, and append those which are valid to tickers list.
        :return: status: (data.Status) Update status
        :exception Timeout: If the request timed out
        """
        logging.info('Initializing data...')

        for stock in self.config.stocks:  # Initialize stocks
            self.fetch_stock(self.config.currency, stock)
        for crypto in self.config.cryptos:  # Initialize cryptos
            self.fetch_crypto(self.config.currency, crypto)
        # Wait until all tickers are initialized
        while len(self.stocks + self.cryptos) < self.valid_tickers:
            time.sleep(0.1)

        self.date = self.get_date()
        self.time = self.get_time()
        return Status.SUCCESS

    def update(self) -> Status:
        """
        Update tickers' prices, date, and time.
        :return: status: (data.Status) Update status
        """
        for ticker in self.stocks + self.cryptos:
            self.update_ticker(ticker)
        self.last_updated = time.time()

        return Status.SUCCESS

    def update_clock(self):
        """Update date & time"""
        self.date = self.get_date()
        self.time = self.get_time()

    @multitasking.task
    def fetch_stock(self, currency: str, symbol: str):
        """
        Fetch stock's data
        :param symbol: Stock symbol
        :param currency: Stock's prices currency
        """
        stock = Stock(currency, symbol)
        if stock.valid:
            self.stocks.append(stock)
        else:
            self.valid_tickers -= 1

    @multitasking.task
    def fetch_crypto(self, currency: str, symbol: str):
        """
        Fetch crypto's data
        :param symbol: Crypto symbol
        :param currency: Crypto's prices currency
        """
        crypto = Crypto(currency, symbol)
        if crypto.valid:
            self.cryptos.append(crypto)
        else:
            self.valid_tickers -= 1

    @multitasking.task
    def update_ticker(self, ticker: Ticker):
        """
        Update ticker's data
        :param ticker: Ticker object to update
        """
        ticker.update()

    def get_time(self) -> str:
        """
        Get current time as a string
        :return: time: Current time
        """
        return time.strftime(self.time_format)

    @staticmethod
    def get_date() -> str:
        """
        Get current date as a string
        :return: date: Current date
        """
        return time.strftime(DATE_FORMAT)

    def should_update(self) -> bool:
        """
        Returns Boolean value to determine if tickers should be updated.
        i.e. If 10 minutes have passed since data was last fetched, an update is needed.
        :return: should_update:
        """
        logging.info('Checking for update')
        time_delta = time.time() - self.last_updated
        return time_delta >= UPDATE_RATE
