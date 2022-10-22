import sys

import pytest

from config.matrix_config import MatrixConfig


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
