import pytest
import sys
import logging
import time
from data.ticker import Ticker
from data.status import Status
from constants import UPDATE_RATE


@pytest.mark.skipif(not sys.platform.startswith('linux'), reason='Requires Linux')
class TestTicker:
    def setup_method(self):
        self.ticker = Ticker('TSLA', 'USD')

    def teardown_method(self):
        del self.ticker

    def test_update(self, caplog):
        caplog.clear()
        with caplog.at_level(logging.DEBUG):
            status = self.ticker.update(True)
        assert status == Status.SUCCESS
        assert f'Fetching new data for {self.ticker.symbol}.' in caplog.text

    def test_get_name(self):
        name = self.ticker.get_name()
        assert name == 'Tesla, Inc.'

    def test_get_current_price(self):
        current_price = self.ticker.get_current_price()
        assert isinstance(current_price, float)

    def test_get_previous_close_price(self):
        prev_close_price = self.ticker.get_previous_close_price()
        assert isinstance(prev_close_price, float)

    def test_get_value_change(self):
        value_change = self.ticker.get_value_change()
        assert isinstance(value_change, float)

    def test_get_percentage_change(self):
        pct_change = self.ticker.get_percentage_change()
        assert isinstance(pct_change, str)
        assert '%' in pct_change

    def test_get_chart_prices(self):
        chart_prices = self.ticker.get_chart_prices()
        assert isinstance(chart_prices, list)
        assert len(chart_prices) > 0

    @pytest.mark.slow
    def test_should_update(self):
        time.sleep(UPDATE_RATE)
        assert self.ticker.should_update() is True
