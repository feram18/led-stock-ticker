import unittest
import sys
from unittest import TestCase
from config.matrix_config import MatrixConfig
from constants import DEFAULT_STOCKS, DEFAULT_CRYPTOS, TWELVE_HOURS_FORMAT, TWENTY_FOUR_HOURS_FORMAT


@unittest.skipUnless(sys.platform.startswith('linux'), 'Requires Linux')
class TestConfig(TestCase):
    def setUp(self) -> None:
        self.config = MatrixConfig(64, 32)

    def test_format_cryptos(self):
        cryptos = ['XLM', 'BNB', 'XRP']
        formatted_cryptos = self.config.format_cryptos(cryptos)
        self.assertListEqual(formatted_cryptos, ['XLM-USD', 'BNB-USD', 'XRP-USD'])

    def test_format_cryptos_2(self):
        formatted_cryptos = self.config.format_cryptos([])
        self.assertListEqual(formatted_cryptos, [])

    def test_validate_cryptos(self):
        cryptos = ['XLM', 'BNB', 'XRP']
        validated_cryptos = self.config.validate_cryptos(cryptos)
        self.assertListEqual(validated_cryptos, cryptos)

    def test_validate_cryptos_2(self):
        invalid_cryptos = [12, 35, 85]
        validated_cryptos = self.config.validate_cryptos(invalid_cryptos)
        self.assertListEqual(validated_cryptos, DEFAULT_CRYPTOS)

    def test_validate_cryptos_3(self):
        partly_valid_cryptos = ['BTC', 45, 'ETH']
        validated_cryptos = self.config.validate_cryptos(partly_valid_cryptos)
        self.assertListEqual(validated_cryptos, ['BTC', 'ETH'])

    def test_validate_cryptos_4(self):
        cryptos = 'LTC'
        validated_cryptos = self.config.validate_cryptos(cryptos)
        self.assertListEqual(validated_cryptos, [cryptos])

    def test_validate_stocks(self):
        stocks = ['AMD', 'GE', 'AAPL']
        validated_stocks = self.config.validate_stocks(stocks)
        self.assertEqual(validated_stocks, stocks)

    def test_validate_stocks_2(self):
        stocks = 'VZ'
        validated_stocks = self.config.validate_stocks(stocks)
        self.assertListEqual(validated_stocks, [stocks])

    def test_validate_stocks_3(self):
        invalid_stocks = [12, 35, 85]
        validated_stocks = self.config.validate_stocks(invalid_stocks)
        self.assertListEqual(validated_stocks, DEFAULT_STOCKS)

    def test_validate_stocks_4(self):
        partly_valid_stocks = ['C', 35, 'GE']
        validated_stocks = self.config.validate_stocks(partly_valid_stocks)
        self.assertListEqual(validated_stocks, ['C', 'GE'])

    def test_validate_currency(self):
        currency = 'EUR'
        validated_currency = self.config.validate_currency(currency)
        self.assertEqual(validated_currency, currency)

    def test_validate_currency_2(self):
        validated_currency = self.config.validate_currency('INVALID_CURRENCY')
        self.assertEqual(validated_currency, 'USD')  # Default Currency = USD

    def test_set_time_format(self):
        clock_format = '12h'
        validated_time_format = self.config.set_time_format(clock_format)
        self.assertEqual(validated_time_format, TWELVE_HOURS_FORMAT)

    def test_set_time_format_2(self):
        clock_format = '24h'
        validated_time_format = self.config.set_time_format(clock_format)
        self.assertEqual(validated_time_format, TWENTY_FOUR_HOURS_FORMAT)

    def test_set_time_format_3(self):
        invalid_clock_format = 'INVALID'
        validated_time_format = self.config.set_time_format(invalid_clock_format)
        self.assertEqual(validated_time_format, TWELVE_HOURS_FORMAT)  # Default Time Format = 12h
