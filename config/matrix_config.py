import logging
from typing import List

from config.layout import Layout
from constants import CONFIG_FILE, CLOCK_FORMATS, TWELVE_HOURS_FORMAT, TWENTY_FOUR_HOURS_FORMAT, \
    DEFAULT_UPDATE_RATE, DEFAULT_ROTATION_RATE
from data.currency import CURRENCIES
from util.utils import read_json


class MatrixConfig:
    """
    Configuration class

    Arguments:
        width (int):                Matrix width
        height (int):               Matrix height

    Attributes:
        layout (Layout):           Layout instance
        config (dict):              Configurations dictionary
        cryptos (list):            List of cryptos
        stocks (list):             List of stocks
        currency (str):            Currency prices will be displayed on
        time_format (str):         Clock's time format
        date_format (str):         Date format
        update_rate (float):        Update rate
        rotation_rate (float):      Rotation rate
    """

    def __init__(self, width: int, height: int):
        self.layout: Layout = Layout(width, height)
        self.config: dict = read_json(CONFIG_FILE)
        self.cryptos: List[str] = self.validate_tickers(self.config['tickers']['cryptos'])
        self.cryptos: List[str] = self.format_cryptos(self.cryptos)
        self.stocks: List[str] = self.validate_tickers(self.config['tickers']['stocks'])
        self.currency: str = self.validate_currency(self.config['currency'])
        self.time_format: str = self.set_time_format(self.config['clock_format'].lower())
        self.date_format: str = self.config['date_format']
        self.update_rate: float = self.validate_update_rate(self.config['update_rate'])
        self.rotation_rate: float = self.validate_rotation_rate(self.config['rotation_rate'])

    @staticmethod
    def format_cryptos(cryptos: List[str]) -> list:
        """
        Append -USD postfix to cryptocurrencies.
        :param cryptos: (list) List of cryptos to format
        :return: result: (list) Formatted list of cryptos
        """
        return [f'{crypto}-USD' for crypto in cryptos]

    @staticmethod
    def validate_tickers(tickers: List[str] or str) -> list:
        """
        Determine if tickers on config are an instance of a list (several tickers) or a single instance of a string (one
        ticker).
        :param tickers: (list or str) List of tickers to validate
        :return validated_tickers: (list) Validated list of tickers
        """
        if isinstance(tickers, str) and 0 < len(tickers) < 6:
            return [tickers]
        elif isinstance(tickers, list):
            validated_tickers = [ticker for ticker in tickers if isinstance(ticker, str) and 0 < len(tickers) < 6]
            if len(validated_tickers) > 0:
                return validated_tickers
        return []

    @staticmethod
    def validate_currency(currency: str) -> str:
        """
        Determine if selected currency is supported. Else, set to default value (USD).
        :param currency: (str) Currency to validate
        :return currency: (str) Validated currency
        """
        if currency not in CURRENCIES:
            logging.warning(f'{currency} is not supported. Setting currency to USD.')
            return 'USD'
        return currency

    def set_time_format(self, clock_format: str) -> str:
        """
        Determine if clock format is an accepted value (12h or 24h). Else, set to default value (12h).
        :param clock_format: (str) Clock format
        :return time_format: (str) Time format
        """
        if clock_format not in CLOCK_FORMATS:
            logging.warning('Invalid clock format. Setting clock format to 12h.')
            self.time_format = '12h'
        else:
            self.time_format = clock_format
        return TWENTY_FOUR_HOURS_FORMAT if self.time_format == '24h' else TWELVE_HOURS_FORMAT

    @staticmethod
    def validate_update_rate(update_rate: int) -> int:
        """
        Determine if the update rate value provided by user is valid
        :param update_rate: (int) update rate in seconds
        :return: validated_rate: (int) Validated update rate in seconds
        """
        if not isinstance(update_rate, int) or update_rate <= 60:
            return DEFAULT_UPDATE_RATE
        return update_rate

    @staticmethod
    def validate_rotation_rate(rotation_rate: int) -> int:
        """
        Determine if the rotation rate value provided by user is valid
        :param rotation_rate: (int) rotation rate in seconds
        :return: validated_rate: (int) Validated rotation rate in seconds
        """
        if not isinstance(rotation_rate, int) or rotation_rate < 5:
            return DEFAULT_ROTATION_RATE
        return rotation_rate
