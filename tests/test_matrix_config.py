import sys

import pytest

from config.matrix_config import MatrixConfig
from constants import TWELVE_HOURS_FORMAT, TWENTY_FOUR_HOURS_FORMAT, DEFAULT_UPDATE_RATE, DEFAULT_ROTATION_RATE


@pytest.mark.skipif(not sys.platform.startswith('linux'), reason='Requires Linux')
class TestMatrixConfig:
    def setup_method(self):
        self.config = MatrixConfig(64, 32)

    def teardown_method(self):
        del self.config

    def test_format_cryptos(self):
        cryptos = ['XLM', 'BNB', 'XRP']
        formatted_cryptos = self.config.format_cryptos(cryptos)
        assert formatted_cryptos == ['XLM-USD', 'BNB-USD', 'XRP-USD']

    def test_format_cryptos_2(self):
        formatted_cryptos = self.config.format_cryptos([])
        assert formatted_cryptos == []

    def test_validate_tickers(self):
        tickers = ['XLM', 'BNB', 'XRP']
        validated_tickers = self.config.validate_tickers(tickers)
        assert validated_tickers == tickers

    def test_validate_tickers_2(self):
        invalid_tickers = [12, 35, 85]
        validated_tickers = self.config.validate_tickers(invalid_tickers)
        assert validated_tickers == []

    def test_validate_tickers_3(self):
        partly_valid_tickers = ['AAPL', 45, 'ETH']
        validated_tickers = self.config.validate_tickers(partly_valid_tickers)
        assert validated_tickers == ['AAPL', 'ETH']

    def test_validate_tickers_4(self):
        tickers = 'LTC'
        validated_tickers = self.config.validate_tickers(tickers)
        assert validated_tickers == [tickers]

    def test_validate_currency(self):
        currency = 'EUR'
        validated_currency = self.config.validate_currency(currency)
        assert validated_currency == currency

    def test_validate_currency_2(self):
        validated_currency = self.config.validate_currency('INVALID_CURRENCY')
        assert validated_currency == 'USD'  # Default Currency = USD

    def test_set_time_format(self):
        clock_format = '12h'
        validated_time_format = self.config.set_time_format(clock_format)
        assert validated_time_format == TWELVE_HOURS_FORMAT

    def test_set_time_format_2(self):
        clock_format = '24h'
        validated_time_format = self.config.set_time_format(clock_format)
        assert validated_time_format == TWENTY_FOUR_HOURS_FORMAT

    def test_set_time_format_3(self):
        invalid_clock_format = 'INVALID'
        validated_time_format = self.config.set_time_format(invalid_clock_format)
        assert validated_time_format == TWELVE_HOURS_FORMAT  # Default Time Format = 12h

    def test_validate_update_rate(self):
        update_rate = 420  # Seconds
        validated_rate = self.config.validate_update_rate(update_rate)
        assert validated_rate == update_rate

    def test_validate_update_rate_2(self):
        invalid_rate = 60
        validated_rate = self.config.validate_update_rate(invalid_rate)
        assert validated_rate == DEFAULT_UPDATE_RATE

    def test_validate_update_rate_3(self):
        invalid_input = "15"
        validated_rate = self.config.validate_update_rate(invalid_input)
        assert validated_rate == DEFAULT_UPDATE_RATE

    def test_validate_rotation_rate(self):
        rotation_rate = 15
        validated_rate = self.config.validate_rotation_rate(rotation_rate)
        assert validated_rate == rotation_rate

    def test_validate_rotation_rate_2(self):
        invalid_rate = 4
        validated_rate = self.config.validate_rotation_rate(invalid_rate)
        assert validated_rate == DEFAULT_ROTATION_RATE

    def test_validate_rotation_rate_3(self):
        invalid_input = "10"
        validated_rate = self.config.validate_rotation_rate(invalid_input)
        assert validated_rate == DEFAULT_ROTATION_RATE
