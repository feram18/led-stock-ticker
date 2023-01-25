import logging

from data.crypto import Crypto
from data.status import Status


class TestCrypto:
    def setup_method(self):
        self.crypto = Crypto('ETH-USD', 'USD')

    def teardown_method(self):
        del self.crypto

    def test_initialize(self):
        # Tests that name no longer contains ' USD' suffix
        assert ' USD' not in self.crypto.name

    def test_update(self):
        status = self.crypto.update()
        assert status == Status.SUCCESS

    def test_update_2(self, caplog):
        caplog.clear()
        with caplog.at_level(logging.DEBUG):
            self.crypto.update()
        assert f'Fetching new data for {self.crypto.symbol}.' in caplog.text

    def test_get_price(self):
        current_price = self.crypto.get_price(self.crypto.yf_ticker.basic_info.last_price)
        assert isinstance(current_price, float)

    def test_get_prev_close(self):
        prev_close_price = self.crypto.get_prev_close()
        assert isinstance(prev_close_price, float)

    def test_get_chart_prices(self):
        chart_prices = self.crypto.get_chart_prices()
        assert isinstance(chart_prices, list)

    def test_get_chart_prices_2(self):
        chart_prices = self.crypto.get_chart_prices()
        assert len(chart_prices) > 0
