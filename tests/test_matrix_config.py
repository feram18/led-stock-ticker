import constants
from config.matrix_config import MatrixConfig


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

    def test_format_forex(self):
        forex = ['USD/EUR', 'CAD/MXN', 'AUD/GBP']
        formatted_forex = self.config.format_forex(forex)
        assert formatted_forex == ['USDEUR=X', 'CADMXN=X', 'AUDGBP=X']

    def test_format_forex_2(self):
        formatted_forex = self.config.format_cryptos([])
        assert formatted_forex == []

    def test_get_time_format(self):
        fmt = self.config.get_time_format('12h')
        assert fmt == constants.TWELVE_HOURS_FORMAT

    def test_get_time_format_2(self):
        fmt = self.config.get_time_format('24h')
        assert fmt == constants.TWENTY_FOUR_HOURS_FORMAT

    def test_get_time_format_3(self):
        fmt = self.config.get_time_format('other')
        assert fmt == constants.TWELVE_HOURS_FORMAT
