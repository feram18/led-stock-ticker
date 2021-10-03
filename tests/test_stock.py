import pytest
import sys
import logging
from PIL.Image import Image
from data.status import Status
from data.stock import Stock


@pytest.mark.skipif(not sys.platform.startswith('linux'), reason='Requires Linux')
class TestStock:
    def setup_method(self):
        self.stock = Stock('TSLA', 'USD')

    def teardown_method(self):
        del self.stock

    def test_update(self):
        status = self.stock.update(True)
        assert status == Status.SUCCESS

    def test_update_2(self, caplog):
        caplog.clear()
        with caplog.at_level(logging.DEBUG):
            self.stock.update(True)
        assert f'Fetching new data for {self.stock.symbol}.' in caplog.text

    def test_get_name(self):
        name = self.stock.get_name()
        assert name == 'Tesla, Inc.'

    def test_get_current_price(self):
        current_price = self.stock.get_current_price()
        assert isinstance(current_price, float)

    def test_get_previous_close_price(self):
        prev_close_price = self.stock.get_previous_close_price()
        assert isinstance(prev_close_price, float)

    def test_get_value_change(self):
        value_change = self.stock.get_value_change()
        assert isinstance(value_change, float)

    def test_get_percentage_change(self):
        pct_change = self.stock.get_percentage_change()
        assert isinstance(pct_change, str)

    def test_get_percentage_change_2(self):
        pct_change = self.stock.get_percentage_change()
        assert '%' in pct_change

    def test_get_chart_prices(self):
        chart_prices = self.stock.get_chart_prices()
        assert isinstance(chart_prices, list)

    def test_get_chart_prices_2(self):
        chart_prices = self.stock.get_chart_prices()
        assert len(chart_prices) > 0

    def test_get_logo(self):
        logo = self.stock.get_logo()
        assert isinstance(logo, Image)
