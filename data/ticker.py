import logging
from dataclasses import dataclass, field
from typing import List

import yahooquery
from PIL import Image
from requests import Timeout

from constants import DEFAULT_CURRENCY
from data.status import Status
from util.utils import convert_currency


@dataclass
class Ticker:
    symbol: str
    currency: str = DEFAULT_CURRENCY
    yq_ticker: yahooquery.Ticker = field(init=False)
    quote: dict = field(init=False)
    name: str = field(init=False)
    price: float = field(init=False)
    prev_close: float = field(init=False)
    value_change: float = field(init=False)
    pct_change: str = field(init=False)
    chart_prices: List[float] = field(default_factory=list)
    img: Image = None
    valid: bool = True
    status: Status = Status.SUCCESS

    def __post_init__(self):
        try:
            self.initialize()
        except (AttributeError, KeyError, TypeError):
            logging.error(f'No data available for {self.symbol}.')
            self.valid = False
            return Status.FAIL
        except Timeout:
            return Status.NETWORK_ERROR

    def initialize(self):
        """
        Setup ticker's initial data.
        :return status: Update status
        :exception KeyError: If incorrect data type is provided as an argument. Can occur when a ticker is not valid.
        :exception Timeout: If the request timed out
        """
        logging.debug(f'Fetching initial data for {self.symbol}.')
        self.yq_ticker = yahooquery.Ticker(self.symbol,
                                           status_forcelist=[404, 429, 500, 502, 503, 504],
                                           validate=True)
        self.quote = self.yq_ticker.quotes.get(self.symbol.upper())
        self.name = self.quote.get('shortName')
        self.price = self.get_price(self.quote.get('regularMarketPrice'))
        self.prev_close = self.quote.get('regularMarketPreviousClose')
        self.value_change = float(format(self.quote.get('regularMarketChange'), '.2f'))
        self.pct_change = f'{float(self.quote.get("regularMarketChangePercent")):.2f}%'
        self.chart_prices = self.get_chart_prices()

    def update(self) -> Status:
        """
        Update only the data that may have changed since last update.
        i.e. Exclude the ticker's name and previous day close price.
        :return status: Update status
        :exception Timeout: If the request timed out
        """
        logging.debug(f'Fetching new data for {self.symbol}.')

        try:
            self.quote = self.yq_ticker.quotes.get(self.symbol.upper())
            self.price = self.get_price(self.quote.get('regularMarketPrice'))
            self.value_change = float(format(self.quote.get('regularMarketChange'), '.2f'))
            self.pct_change = f'{float(self.quote.get("regularMarketChangePercent")):.2f}%'
            self.chart_prices = self.get_chart_prices()
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

    def get_chart_prices(self) -> List[float]:
        """
        Fetch historical market data for chart.
        :return: chart_prices: List of historical prices
        """
        period, attempts = 1, 0
        prices = []
        while len(prices) < 100 and attempts < 5:
            prices = self.yq_ticker.history(interval='1m', period=f'{period}d')['close'].tolist()
            period += 1  # Go back an additional day
            attempts += 1
        if not prices:
            self.valid = False
            prices.append(0.0)
        return prices
