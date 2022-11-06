from dataclasses import dataclass

from data.ticker import Ticker
from util.utils import convert_currency


@dataclass
class Stock(Ticker):
    logo_url: str = None

    def initialize(self):
        super(Stock, self).initialize()
        self.logo_url = self.yf_ticker.info.get('logo_url', None)
        self.name = self.name\
            .replace('Company', '')\
            .replace('Corporation', '')\
            .replace('Holdings', '')\
            .replace('Incorporated', '')\
            .replace('Inc', '')\
            .replace('.com', '')\
            .replace('(The)', '') \
            .rstrip('& ')\
            .rstrip('. ')\
            .rstrip(', ')\
            .rstrip()

    def get_prev_close(self) -> float:
        """
        Fetch the stock's previous close price.
        If currency is not set to USD, convert value to user-selected currency.
        :return: prev_close: Previous day's close price
        :exception KeyError: If incorrect data type is provided as an argument. Can occur when a ticker is not valid.
        """
        prev_close = self.yf_ticker.info.get('regularMarketPreviousClose', 0.00)
        if self.currency == 'USD':
            return prev_close
        return convert_currency('USD', self.currency, prev_close)
