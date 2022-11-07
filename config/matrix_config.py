import logging
import sys
from dataclasses import dataclass, field
from typing import List

from jsonschema import Draft7Validator, ValidationError

from config.layout import Layout
from constants import DEFAULT_CURRENCY, TWELVE_HOURS_FORMAT, DEFAULT_DATE_FORMAT, DEFAULT_ROTATION_RATE, \
    DEFAULT_UPDATE_RATE, CONFIG_SCHEMA, CONFIG_FILE, TWENTY_FOUR_HOURS_FORMAT
from util.utils import read_json


@dataclass
class MatrixConfig:
    width: int
    height: int
    layout: Layout = field(init=False)
    schema: dict = field(default_factory=dict)
    config: dict = field(default_factory=dict)
    stocks: List[str] = field(default_factory=list)
    cryptos: List[str] = field(default_factory=list)
    forex: List[str] = field(default_factory=list)
    currency: str = DEFAULT_CURRENCY
    clock_format: str = TWELVE_HOURS_FORMAT
    date_format: str = DEFAULT_DATE_FORMAT
    rotation_rate: float = DEFAULT_ROTATION_RATE
    update_rate: float = DEFAULT_UPDATE_RATE

    def __post_init__(self):
        self.layout = Layout(self.width, self.height)
        self.schema = read_json(CONFIG_SCHEMA)
        self.config = read_json(CONFIG_FILE)
        self.validate_config()

    def validate_config(self):
        v = None
        try:
            v = Draft7Validator(self.schema)
            v.validate(self.config)
            self.stocks = self.config['tickers']['stocks']
            self.cryptos = self.format_cryptos(self.config['tickers']['cryptos'])
            self.forex = self.format_forex(self.config['tickers']['forex'])
            self.currency = self.config['options']['currency']
            self.clock_format = self.get_time_format(self.config['options']['clock_format'])
            self.date_format = self.config['options']['date_format']
            self.rotation_rate = self.config['options']['rotation_rate']
            self.update_rate = self.config['options']['update_rate'] * 60  # convert to minutes
            self.layout.show_logos = self.config['options']['show_logos'] if self.height > 16 else False
        except ValidationError:
            errors = sorted(v.iter_errors(self.config), key=lambda e: e.path)
            logging.error('Invalid config.json file:')
            for error in errors:
                logging.error(error.message)
            sys.exit(1)

    @staticmethod
    def format_cryptos(cryptos: List[str]) -> list:
        """
        Append -USD postfix to cryptocurrencies.
        :param cryptos: (list) List of cryptos to format
        :return: result: (list) Formatted symbols
        """
        return [f'{crypto}-USD' for crypto in cryptos]

    @staticmethod
    def format_forex(forex: List[str]) -> list:
        """
        Format the forex symbol to the format needed for yfinance (i.e. USD/EUR -> USDEUR=X)
        :param forex: list of forex symbols
        :return: result: (list) Formatted symbols
        """
        lst = []
        for pair in forex:
            currency_from, currency_to = pair.split('/')
            lst.append(f'{currency_from}{currency_to}=X')
        return lst

    @staticmethod
    def get_time_format(fmt: str) -> str:
        """
        Get the appropriate time format based on input (12h or 24h). Else, set to default value (12h).
        :param fmt: format to get
        :return time_format: (str) Time format
        """
        return TWENTY_FOUR_HOURS_FORMAT if fmt == '24h' else TWELVE_HOURS_FORMAT
