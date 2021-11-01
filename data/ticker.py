import logging
import yfinance as yf
from dataclasses import dataclass, field
from abc import abstractmethod
from typing import List
from requests.exceptions import Timeout
from data.status import Status
from utils import convert_currency


@dataclass
class Ticker:
    currency: str
    symbol: str
    yf_ticker: yf.Ticker = field(init=False)
    name: str = field(init=False)
    price: float = field(init=False)
    prev_close: float = field(init=False)
    value_change: float = field(init=False)
    pct_change: str = field(init=False)
    chart_prices: List[float] = field(default_factory=list)
    valid: bool = True
    status: Status = Status.SUCCESS

    def __post_init__(self):
        self.initialize()

    def initialize(self) -> Status:
        """
        Setup ticker's initial data.
        :return status: Update status
        :exception KeyError: If incorrect data type is provided as an argument. Can occur when a ticker is not valid.
        :exception Timeout: If the request timed out
        """
        logging.debug(f'Fetching initial data for {self.symbol}.')
        try:
            self.yf_ticker = yf.Ticker(self.symbol)
            self.name = self.yf_ticker.info['shortName'].replace(' USD', '')
            self.price = self.get_price(self.yf_ticker.info.get('regularMarketPrice', 0.00))
            self.prev_close = self.get_prev_close(self.yf_ticker)
            self.value_change = float(format((self.price - self.prev_close), '.2f'))
            self.pct_change = f'{100 * (self.value_change / abs(self.prev_close)):.2f}%'
            self.chart_prices = self.get_chart_prices(self.yf_ticker)
        except KeyError:
            logging.error(f'No data available for {self.symbol}.')
            self.valid = False
            return Status.FAIL
        except Timeout:
            return Status.NETWORK_ERROR

    def update(self) -> Status:
        """
        Update only the data that may have changed since last update.
        i.e. Exclude the ticker's name and previous day close price.
        :return status: Update status
        :exception Timeout: If the request timed out
        """
        logging.debug(f'Fetching new data for {self.symbol}.')

        try:
            self.yf_ticker = yf.Ticker(self.symbol)
            self.price = self.get_price(self.yf_ticker.info.get('regularMarketPrice', 0.00))
            self.value_change = float(format((self.price - self.prev_close), '.2f'))
            self.pct_change = f'{100 * (self.value_change / abs(self.prev_close)):.2f}%'
            self.chart_prices = self.get_chart_prices(self.yf_ticker)
            return Status.SUCCESS
        except Timeout:
            return Status.NETWORK_ERROR

    def get_price(self, price: float) -> float:
        """
        Fetch the ticker's current price.
        If currency is not set to USD, convert value to user-selected currency.
        :return: price: Current price
        :exception KeyError: If incorrect data type is provided as an argument. Can occur when a ticker is not valid.
        """
        if self.currency != 'USD':
            price = convert_currency('USD', self.currency, price)
        return float(format(price, '.3f')) if price < 1.0 else float(format(price, '.2f'))

    @abstractmethod
    def get_prev_close(self, ticker: yf.Ticker) -> float:
        ...

    def get_chart_prices(self, ticker: yf.Ticker) -> List[float]:
        """
        Fetch historical market data for chart.
        :return: chart_prices: List of historical prices
        """
        prices = ticker.history(interval='1m', period='1d')['Close'].tolist()
        if len(prices) < 100:
            prices = ticker.history(interval='1m', period='3d')['Close'].tolist()
        elif not prices:
            self.valid = False
            prices.append(0.0)
        return prices
