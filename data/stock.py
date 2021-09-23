import logging
import time
import yfinance as yf
import requests
from requests.exceptions import MissingSchema, Timeout, ConnectionError
from PIL import Image, UnidentifiedImageError
from data.ticker import Ticker
from data.status import Status


class Stock(Ticker):
    """
    Class to represent a Stock object

    Arguments:
        ticker (str):               Ticker string
        currency (str):             Currency prices will be displayed on

    Attributes:
        logo (PIL.Image):           Ticker's company/brand logo
    """
    def __init__(self, ticker: str, currency: str):
        super().__init__(ticker, currency)
        self.logo = None

    def initialize(self) -> Status:
        """
        Setup stock's initial data.
        :return status: (data.Status) Update status
        :exception KeyError: If incorrect data type is provided as an argument. Can occur when a ticker is not valid.
        :exception Timeout: If the request timed out
        """
        logging.debug(f'Fetching initial data for {self.ticker}.')

        try:
            self.data = yf.Ticker(self.ticker)

            self.name = self.get_name()
            self.current_price = self.get_current_price()
            self.prev_close_price = self.get_previous_close_price()
            self.value_change = self.get_value_change()
            self.pct_change = self.get_percentage_change()
            self.chart_prices = self.get_chart_prices()
            self.logo = self.get_logo()

            self.last_updated = time.time()
            self.initialized = True
            return Status.SUCCESS
        except KeyError:
            logging.error(f'No data available for {self.ticker}.')
            self.valid = False
            return Status.FAIL
        except Timeout:
            return Status.NETWORK_ERROR

    def get_logo(self) -> Image:
        """
        Fetch the ticker's logo.
        :return: logo: (PIL.Image)
        :exception MissingSchema: If the URL schema is missing.
        :exception UnidentifiedImageError: If an image cannot be opened and identified
        :exception ConnectionError: If a Connection error occurred
        """
        try:
            logo = Image.open(requests.get(self.data.info['logo_url'], stream=True).raw)
            logo.thumbnail((8, 8), Image.ANTIALIAS)
            return logo.convert('RGB')
        except MissingSchema:
            logging.exception(f'Invalid URL for {self.ticker} logo image provided.')
        except UnidentifiedImageError:
            logging.exception(f'Invalid image format for {self.ticker} logo image.')
        except ConnectionError:
            logging.exception(f'Unable to fetch {self.ticker} logo image.')

    def __str__(self):
        return f'<{self.__class__.__name__} {hex(id(self))}> ' \
               f'Ticker: {self.ticker}; ' \
               f'Full Name: {self.name}; ' \
               f'Previous Day Close Price: {self.prev_close_price}; ' \
               f'Current Price: {self.current_price}; ' \
               f'Value Change: {self.value_change}; ' \
               f'Percentage Change: {self.pct_change}; ' \
               f'Logo: {self.logo};'
