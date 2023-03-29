import logging
import time
from dataclasses import dataclass, field
from typing import List

import multitasking

from matrix.matrix_config import MatrixConfig
from data.crypto import Crypto
from data.forex import Forex
from data.status import Status
from data.stock import Stock
from data.ticker import Ticker
from util.market_status import MarketStatus
from util.utils import market_status


@dataclass
class Data:
    config: MatrixConfig
    date: str = field(init=False)
    time: str = field(init=False)
    market_status: MarketStatus = field(init=False)
    cryptos: List[Ticker] = field(default_factory=list)
    stocks: List[Ticker] = field(default_factory=list)
    forex: List[Forex] = field(default_factory=list)
    valid_tickers: int = 0
    status: Status = Status.SUCCESS
    last_updated: float = None

    def __post_init__(self):
        self.valid_tickers = len(self.config.stocks + self.config.cryptos + self.config.forex)
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

        self.market_status = market_status()
        for stock in self.config.stocks:  # Initialize stocks
            self.fetch_stock(stock, self.config.currency)
        for crypto in self.config.cryptos:  # Initialize cryptos
            self.fetch_crypto(crypto, self.config.currency)
        for forex in self.config.forex:  # Initialize forex
            self.fetch_forex(forex)
        # Wait until all tickers are initialized
        while len(self.stocks + self.cryptos + self.forex) < self.valid_tickers:
            time.sleep(0.1)

        self.date = self.get_date()
        self.time = self.get_time()
        return Status.SUCCESS

    def update(self) -> Status:
        """
        Update tickers' prices, date, and time.
        :return: status: (data.Status) Update status
        """
        logging.debug('Checking for update')
        for ticker in self.stocks + self.cryptos + self.forex:
            self.update_ticker(ticker)
        self.last_updated = time.time()

        return Status.SUCCESS

    def update_clock(self):
        """Update date & time"""
        self.date = self.get_date()
        self.time = self.get_time()

    def update_market_status(self):
        """Update market status"""
        self.market_status = market_status()

    @multitasking.task
    def fetch_stock(self, symbol: str, currency: str):
        """
        Fetch stock's data
        :param symbol: Stock symbol
        :param currency: Stock's prices currency
        """
        stock = Stock(symbol, currency)
        if stock.valid:
            self.stocks.append(stock)
        else:
            self.valid_tickers -= 1
            logging.warning(f'Stock: {stock.symbol} may not be valid.')

    @multitasking.task
    def fetch_crypto(self, symbol: str, currency: str):
        """
        Fetch crypto's data
        :param symbol: Crypto symbol
        :param currency: Crypto's prices currency
        """
        crypto = Crypto(symbol, currency)
        if crypto.valid:
            self.cryptos.append(crypto)
        else:
            self.valid_tickers -= 1
            logging.warning(f'Crypto: {crypto.symbol} may not be valid.')

    @multitasking.task
    def fetch_forex(self, symbol: str):
        """
        Fetch forex rates
        :param symbol: Forex pair
        """
        forex = Forex(symbol)
        if forex.valid:
            self.forex.append(forex)
        else:
            self.valid_tickers -= 1
            logging.warning(f'Forex: {forex.symbol} may not be valid.')

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
        return time.strftime(self.config.clock_format)

    def get_date(self) -> str:
        """
        Get current date as a string
        :return: date: Current date
        """
        return time.strftime(self.config.date_format)

    def should_update(self) -> bool:
        """
        Returns Boolean value to determine if tickers should be updated.
        i.e. If 10 minutes have passed since data was last fetched, an update is needed.
        :return: should_update:
        """
        time_delta = time.time() - self.last_updated
        return time_delta >= self.config.update_rate
