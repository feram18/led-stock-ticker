import logging
from typing import List
from config.layout import Layout
from constants import CONFIG_FILE, DEFAULT_STOCKS, DEFAULT_CRYPTOS, CLOCK_FORMATS, TWELVE_HOURS_FORMAT, \
    TWENTY_FOUR_HOURS_FORMAT
from utils import read_json
from data.currency import currencies


class MatrixConfig:
    """
    Configuration class

    Arguments:
        width (int):                Matrix width
        height (int):               Matrix height

    Attributes:
        layout (Layout):            Layout instance
        config (dict):              Configurations dictionary
        cryptos (list):             List of crypto strings
        stocks (list):              List of stock strings
        currency (str):             Currency prices will be displayed on
        time_format (str):          Clock's time format
    """

    def __init__(self, width: int, height: int):
        # Layout configuration
        self.layout = Layout(width, height)

        # Validate and set configurations
        self.config = read_json(CONFIG_FILE)
        self.cryptos = self.validate_cryptos(self.config['tickers']['cryptos'])
        self.cryptos = self.format_cryptos(self.cryptos)
        self.stocks = self.validate_stocks(self.config['tickers']['stocks'])
        self.currency = self.validate_currency(self.config['currency'])
        self.time_format = self.set_time_format(self.config['clock_format'].lower())

    @staticmethod
    def format_cryptos(cryptos: List[str]) -> list:
        """
        Append -USD postfix to cryptocurrencies.
        :param cryptos: (list) List of cryptos to format
        :return: result: (list) Formatted list of cryptos
        """
        return [f'{crypto}-USD' for crypto in cryptos]

    @staticmethod
    def validate_cryptos(cryptos: List[str] or str) -> list:
        """
        Determine if cryptos on config are an instance of a list (several tickers) or a single instance of a string
        (i.e. one ticker). Else, set cryptos list to default values (BTC, ETH, LTC).
        :param cryptos: (list or str) List of cryptos to validate
        :return validated_cryptos: (list) Validated list of cryptos
        """
        if isinstance(cryptos, str):
            return [cryptos]
        elif isinstance(cryptos, list):
            validated_cryptos = [crypto for crypto in cryptos if isinstance(crypto, str)]
            if len(validated_cryptos) > 0:
                return validated_cryptos
        logging.warning('Cryptos should be an array of tickers or a single ticker string. '
                        f'Using default cryptos, {DEFAULT_CRYPTOS}.')
        return DEFAULT_CRYPTOS

    @staticmethod
    def validate_stocks(stocks: List[str] or str) -> list:
        """
        Determine if stocks on config are an instance of a list (several tickers) or a single instance of a string
        (i.e. one ticker). Else, set stocks list to default values (TSLA, AMZN, MSFT).
        :param stocks: (List[str] or str) List of stocks to validate
        :return result: (list) Validated list of stocks
        """
        if isinstance(stocks, str):
            return [stocks]
        elif isinstance(stocks, list):
            validated_stocks = [stock for stock in stocks if isinstance(stock, str)]
            if len(validated_stocks) > 0:
                return validated_stocks
        logging.warning('Stocks should be an array of tickers or a single ticker string. '
                        f'Using default stocks, {DEFAULT_STOCKS}.')
        return DEFAULT_STOCKS

    @staticmethod
    def validate_currency(currency: str) -> str:
        """
        Determine if selected currency is supported. Else, set to default value (USD).
        :param currency: (str) Currency to validate
        :return currency: (str) Validated currency
        """
        if currency not in currencies:
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
