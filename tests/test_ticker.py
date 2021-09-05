import unittest
from unittest import TestCase
from data.ticker import *


class TestTicker(TestCase):
    def setUp(self) -> None:
        self.ticker = Ticker('TSLA', 'USD')

    def test_update(self):
        with self.assertLogs(level=logging.DEBUG) as cm:
            status = self.ticker.update(True)
        self.assertEqual(status, Status.SUCCESS)
        self.assertIn(f'DEBUG:root:Fetching new data for {self.ticker.ticker}.', cm.output)

    def test_get_name(self):
        name = self.ticker.get_name()
        self.assertEqual(name, 'Tesla, Inc.')

    def test_get_current_price(self):
        current_price = self.ticker.get_current_price()
        self.assertIsInstance(current_price, float)

    def test_get_previous_close_price(self):
        prev_close_price = self.ticker.get_previous_close_price()
        self.assertIsInstance(prev_close_price, float)

    def test_get_value_change(self):
        value_change = self.ticker.get_value_change()
        self.assertIsInstance(value_change, float)

    def test_get_percentage_change(self):
        pct_change = self.ticker.get_percentage_change()
        self.assertIsInstance(pct_change, str)
        self.assertIn('%', pct_change)

    def test_get_chart_prices(self):
        chart_prices = self.ticker.get_chart_prices()
        self.assertIsInstance(chart_prices, list)
        self.assertTrue(len(chart_prices) > 0)

    @unittest.SkipTest
    def test_should_update(self):
        time.sleep(UPDATE_RATE)
        self.assertEqual(self.ticker.should_update(), True)
