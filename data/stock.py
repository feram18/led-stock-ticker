import requests
import logging
import yfinance as yf
from dataclasses import dataclass
from PIL import Image, UnidentifiedImageError
from requests.exceptions import ConnectionError
from data.ticker import Ticker
from utils import convert_currency


@dataclass
class Stock(Ticker):
    logo: Image = None

    def initialize(self):
        super(Stock, self).initialize()
        self.logo = self.get_logo(self.yf_ticker.info.get('logo_url', None))

    def get_prev_close(self, ticker: yf.Ticker) -> float:
        """
        Fetch the stock's previous close price.
        If currency is not set to USD, convert value to user-selected currency.
        :param ticker: Yfinance Ticker instance
        :return: prev_close: Previous day's close price
        :exception KeyError: If incorrect data type is provided as an argument. Can occur when a ticker is not valid.
        """
        prev_close = ticker.info.get('regularMarketPreviousClose', 0.00)
        if self.currency == 'USD':
            return prev_close
        else:
            return convert_currency('USD', self.currency, prev_close)

    def get_logo(self, img_url: str) -> Image:
        """
        Fetch the stock's company logo.
        :param img_url: URL to logo image
        :return: logo: Stock's company logo image
        :exception UnidentifiedImageError: If image cannot be opened/identified
        :exception ConnectionError: If connection error occurred
        """
        if img_url:
            try:
                logo = Image.open(requests.get(img_url, stream=True).raw)
                logo.thumbnail((8, 8), Image.ANTIALIAS)
                return logo.convert('RGB')
            except UnidentifiedImageError:
                logging.exception(f'Invalid image format for {self.symbol} logo image.')
            except ConnectionError:
                logging.exception(f'Unable to fetch {self.symbol} logo image.')
