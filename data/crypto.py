from datetime import datetime, timedelta
from pytz import timezone
from utils import convert_currency
from data.ticker import Ticker
from data.status import Status


class Crypto(Ticker):
    """Class to represent a Crypto object"""

    def get_name(self) -> str:
        """
        Fetch crypto's full name. i.e. BTC -> Bitcoin. Removes 'USD' suffix.
        :return: name: (str) Name
        :exception KeyError: If incorrect data type is provided as an argument. Can occur when a ticker is not valid.
        """
        try:
            name = self.data.info['shortName']
            return name.replace(' USD', '')
        except KeyError:
            self.valid = False
            self.update_status = Status.FAIL
            return ''

    def get_previous_close_price(self) -> float:
        """
        Fetch the crypto's price 24h ago.
        If currency is not set to USD, convert value to user-selected currency.
        :return: prev_close: (float) Previous day's close price
        :exception TypeError: Inappropriate argument type. Occurs when crypto is not valid.
        """
        try:
            prices = self.data.history(interval='1m', period='2d')
            today = datetime.now(timezone('Europe/London'))
            yesterday = today - timedelta(days=1)   # Change to yesterday
            yesterday = yesterday.replace(second=0)
            yesterday = datetime.isoformat(yesterday, sep=' ', timespec='seconds').format('%Y-%m-%d %H:%M:%S%z')
            prev_close = prices.loc[yesterday].Close
            if self.currency != 'USD':
                prev_close = convert_currency('USD', self.currency, prev_close)
            return prev_close
        except TypeError:
            self.valid = False
            self.update_status = Status.FAIL
            return 0.00
