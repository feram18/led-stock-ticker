import logging
import time
import yfinance as yf
from requests.exceptions import Timeout
from data.ticker import Ticker
from data.status import Status


class Crypto(Ticker):
    """Class to represent a Crypto object"""

    def initialize(self) -> Status:
        """
        Setup crypto's initial data.
        :return status: (data.Status) Update status
        :exception KeyError: If incorrect data type is provided as an argument. Can occur when a ticker is not valid.
        :exception Timeout: If the request timed out
        """
        logging.debug(f'Fetching initial data for {self.symbol}.')

        try:
            self.data = yf.Ticker(self.symbol)

            self.name = self.get_name()
            self.current_price = self.get_current_price()
            self.prev_close_price = self.get_previous_close_price()
            self.value_change = self.get_value_change()
            self.pct_change = self.get_percentage_change()
            self.chart_prices = self.get_chart_prices()

            self.last_updated = time.time()
            self.initialized = True
            return Status.SUCCESS
        except KeyError:
            logging.error(f'No data available for {self.symbol}.')
            self.valid = False
            return Status.FAIL
        except Timeout:
            return Status.NETWORK_ERROR

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
