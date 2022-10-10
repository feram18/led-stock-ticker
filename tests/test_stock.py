import sys
import logging

import pytest
from PIL.Image import Image

from data.status import Status
from data.stock import Stock


@pytest.mark.skipif(not sys.platform.startswith('linux'), reason='Requires Linux')
class TestStock:
    def setup_method(self):
        self.stock = Stock('USD', 'AMZN')

    def teardown_method(self):
        del self.stock

    def test_update(self):
        status = self.stock.update()
        assert status == Status.SUCCESS

    def test_update_2(self, caplog):
        caplog.clear()
        with caplog.at_level(logging.DEBUG):
            self.stock.update()
        assert f'Fetching new data for {self.stock.symbol}.' in caplog.text

    def test_get_price(self):
        price = self.stock.get_price(self.stock.yf_ticker.info['regularMarketPrice'])
        assert isinstance(price, float)

    def test_get_prev_close(self):
        prev_close = self.stock.get_prev_close(self.stock.yf_ticker)
        assert isinstance(prev_close, float)

    def test_get_chart_prices(self):
        chart_prices = self.stock.get_chart_prices(self.stock.yf_ticker)
        assert isinstance(chart_prices, list)

    def test_get_chart_prices_2(self):
        chart_prices = self.stock.get_chart_prices(self.stock.yf_ticker)
        assert len(chart_prices) > 0

    def test_get_logo(self):
        logo = self.stock.get_logo(self.stock.yf_ticker.info['logo_url'])
        assert isinstance(logo, Image)

    def test_get_logo_2(self):
        logo = self.stock.get_logo(None)
        assert logo is None
