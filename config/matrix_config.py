import logging
from typing import List
from constants import CONFIG_FILE, LAYOUT_FILE, DEFAULT_STOCKS, DEFAULT_CRYPTOS, CLOCK_FORMATS, TWELVE_HOURS_FORMAT, \
    TWENTY_FOUR_HOURS_FORMAT
from utils import read_json
from data.currency import currencies


class MatrixConfig(object):
    """
    Configuration class

    Arguments:
        width (int):                Matrix width (pixel count)
        height (int):               Matrix height (pixel count)

    Attributes:
        config (dict):              Configurations dictionary
        layout (dict):              Layout dictionary
        stocks (list):              List of stock strings
        cryptos (list):             List of crypto strings
        currency (str):             Currency prices will be displayed on
        time_format (str):          Clock's time format
    """

    def __init__(self, width: int, height: int):
        self.config = read_json(CONFIG_FILE)

        # Matrix dimensions
        self.width = width
        self.height = height

        # Layout configuration
        self.layout = read_json(LAYOUT_FILE.format(self.width, self.height))

        # Validate and set configurations
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
        result = []
        if len(cryptos) > 0:
            for crypto in cryptos:
                result.append(f'{crypto}-USD')
        return result

    @staticmethod
    def validate_cryptos(cryptos: List[str] or str) -> list:
        """
        Determine if cryptos on config are an instance of a list (several tickers) or a single instance of a string
        (i.e. One ticker). Else, set cryptos list to default values (BTC, ETH, LTC).
        :param cryptos: (list or str) List of cryptos to validate
        :return validated_cryptos: (list) Validated list of cryptos
        """
        if isinstance(cryptos, str):
            return [cryptos]
        elif isinstance(cryptos, list):
            validated_cryptos = []
            for crypto in cryptos:
                if isinstance(crypto, str):
                    validated_cryptos.append(crypto)
            if len(validated_cryptos) > 0:
                return validated_cryptos
            else:
                return DEFAULT_CRYPTOS
        else:
            logging.warning('Cryptos should be an array of tickers or a single ticker string. '
                            f'Using default cryptos, {DEFAULT_CRYPTOS}.')
            return DEFAULT_CRYPTOS

    @staticmethod
    def validate_stocks(stocks: List[str] or str) -> list:
        """
        Determine if stocks on config are an instance of a list (several tickers) or a single instance of a string
        (i.e. One tickers). Else, set stocks list to default values (TSLA, AMZN, MSFT).
        :param stocks: (list or str) List of stocks to validate
        :return result: (list) Validated list of stocks
        """
        if isinstance(stocks, str):
            return [stocks]
        elif isinstance(stocks, list):
            validated_stocks = []
            for stock in stocks:
                if isinstance(stock, str):
                    validated_stocks.append(stock)
            if len(validated_stocks) > 0:
                return validated_stocks
            else:
                return DEFAULT_STOCKS
        else:
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
        else:
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
