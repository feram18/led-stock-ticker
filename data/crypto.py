import yfinance as yf
from dataclasses import dataclass
from datetime import datetime, timedelta
from pytz import timezone
from data.ticker import Ticker
from data.status import Status
from utils import convert_currency


@dataclass
class Crypto(Ticker):
    def get_prev_close(self, ticker: yf.Ticker) -> float:
        """
        Fetch the crypto's price 24h ago.
        If currency is not set to USD, convert value to user-selected currency.
        :param ticker: Yfinance Ticker instance
        :return: prev_close: Previous day's close price
        :exception TypeError: Inappropriate argument type. Occurs when crypto is not valid.
        """
        try:
            prices = ticker.history(interval='1m', period='2d')
            today = datetime.now(timezone('Europe/London'))  # Timezone used by yfinance library
            yesterday = today - timedelta(days=1)
            yesterday = yesterday.replace(second=0)
            yesterday = datetime.isoformat(yesterday, sep=' ', timespec='seconds').format('%Y-%m-%d %H:%M:%S%z')
            prev_close = prices.loc[yesterday].Close
            if self.currency != 'USD':
                prev_close = convert_currency('USD', self.currency, prev_close)
            return prev_close
        except TypeError:
            self.valid = False
            self.status = Status.FAIL
