import logging

from data.status import Status
from data.stock import Stock


class TestStock:
    def setup_method(self):
        self.stock = Stock('AMZN', 'USD')

    def teardown_method(self):
        del self.stock

    def test_initialize(self):
        # Tests if name was simplified
        removed = [
            'Company',
            'Corporation',
            'Holdings',
            'Incorporated',
            'Inc',
            '.com',
            '(The)'
        ]
        for i in removed:
            assert i not in self.stock.name

    def test_update(self):
        status = self.stock.update()
        assert status == Status.SUCCESS

    def test_update_2(self, caplog):
        caplog.clear()
        with caplog.at_level(logging.DEBUG):
            self.stock.update()
        assert f'Fetching new data for {self.stock.symbol}.' in caplog.text

    def test_get_price(self):
        price = self.stock.get_price(self.stock.yf_ticker.basic_info.last_price)
        assert isinstance(price, float)

    def test_get_prev_close(self):
        prev_close = self.stock.get_prev_close()
        assert isinstance(prev_close, float)

    def test_get_chart_prices(self):
        chart_prices = self.stock.get_chart_prices()
        assert isinstance(chart_prices, list)

    def test_get_chart_prices_2(self):
        chart_prices = self.stock.get_chart_prices()
        assert len(chart_prices) > 0
