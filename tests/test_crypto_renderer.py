import pytest
import sys
from renderer.crypto import CryptoRenderer


@pytest.mark.skipif(not sys.platform.startswith('linux'), reason='Requires Linux')
class TestCryptoRenderer:
    def test_format_symbol(self):
        result = CryptoRenderer.format_symbol('BTC-USD')
        assert result == 'BTC'

    def test_format_symbol_2(self):
        result = CryptoRenderer.format_symbol('BTC')
        assert result == 'BTC'
