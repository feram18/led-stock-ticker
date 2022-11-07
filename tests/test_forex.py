import logging

from data.forex import Forex
from data.status import Status


class TestForex:
    def setup_method(self):
        self.forex = Forex('USDEUR=X')

    def teardown_method(self):
        del self.forex

    def test_update(self):
        status = self.forex.update()
        assert status == Status.SUCCESS

    def test_update_2(self, caplog):
        caplog.clear()
        with caplog.at_level(logging.DEBUG):
            self.forex.update()
        assert f'Fetching new data for {self.forex.symbol}.' in caplog.text

    def test_get_price(self):
        current_price = self.forex.get_price(self.forex.yf_ticker.info['regularMarketPrice'])
        assert isinstance(current_price, float)

    def test_get_prev_close(self):
        prev_close_price = self.forex.get_prev_close()
        assert isinstance(prev_close_price, float)

    def test_get_chart_prices(self):
        chart_prices = self.forex.get_chart_prices()
        assert isinstance(chart_prices, list)

    def test_get_chart_prices_2(self):
        chart_prices = self.forex.get_chart_prices()
        assert len(chart_prices) > 0
