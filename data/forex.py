from dataclasses import dataclass, field
from typing import List

from constants import FLAG_URL
from data.ticker import Ticker


@dataclass
class Forex(Ticker):
    img_url: List[str] = field(init=False)

    def initialize(self):
        super(Forex, self).initialize()
        if self.valid:
            self.img_url = [FLAG_URL.format(i) for i in self.name.lower().split('/')]

    def get_prev_close(self) -> float:
        """
        Fetch the stock's previous close price.
        If currency is not set to USD, convert value to user-selected currency.
        :return: prev_close: Previous day's close price
        :exception KeyError: If incorrect data type is provided as an argument. Can occur when a ticker is not valid.
        """
        return self.yf_ticker.info.get('regularMarketPreviousClose', 0.00)
