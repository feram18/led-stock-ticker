import pytest
import sys
from data.crypto import Crypto


@pytest.mark.skipif(not sys.platform.startswith('linux'), reason='Requires Linux')
class TestCrypto:
    def setup_method(self):
        self.crypto = Crypto('ETH-USD', 'USD')

    def teardown_method(self):
        del self.crypto

    def test_get_name(self):
        name = self.crypto.get_name()
        assert name == 'Ethereum'

    def test_get_current_price(self):
        current_price = self.crypto.get_current_price()
        assert isinstance(current_price, float)

    def test_get_previous_close_price(self):
        prev_close_price = self.crypto.get_previous_close_price()
        assert isinstance(prev_close_price, float)

    def test_get_value_change(self):
        value_change = self.crypto.get_value_change()
        assert isinstance(value_change, float)

    def test_get_percentage_change(self):
        pct_change = self.crypto.get_percentage_change()
        assert isinstance(pct_change, str)
        assert '%' in pct_change

    def test_get_chart_prices(self):
        chart_prices = self.crypto.get_chart_prices()
        assert isinstance(chart_prices, list)
        assert len(chart_prices) > 0