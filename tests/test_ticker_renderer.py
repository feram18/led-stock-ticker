import unittest
import sys
from unittest import TestCase
from renderer.ticker import TickerRenderer
from data.crypto import Crypto
from data.stock import Stock
from data.color import Color


@unittest.skipUnless(sys.platform.startswith("linux"), "Requires Linux")
class TestTickerRenderer(TestCase):
    def test_format_ticker(self):
        result = TickerRenderer.format_symbol('BTC-USD')
        self.assertEqual(result, 'BTC')

    def test_format_ticker_2(self):
        result = TickerRenderer.format_symbol('TSLA')
        self.assertEqual(result, 'TSLA')

    def test_format_price(self):
        result = TickerRenderer.format_price('USD', 78.23)
        self.assertEqual(result, '$78.23')

    def test_format_price_2(self):
        result = TickerRenderer.format_price('PLN', 78.23)
        self.assertEqual(result, 'zł78.23')

    def test_set_change_color(self):
        color = TickerRenderer.set_change_color(78.23)
        self.assertEqual(color, Color.GREEN)

    def test_set_change_color_2(self):
        color = TickerRenderer.set_change_color(-14.68)
        self.assertEqual(color, Color.RED)

    def test_set_change_color_3(self):
        color = TickerRenderer.set_change_color(0)
        self.assertEqual(color, Color.GREEN)

    def test_set_market_status_color(self):
        color = TickerRenderer.set_market_status_color(True)
        self.assertEqual(color, Color.RED)

    def test_set_market_status_color_2(self):
        color = TickerRenderer.set_market_status_color(False)
        self.assertEqual(color, Color.GREEN)

    def test_market_status_closed(self):
        crypto = Crypto('BTC-USD', 'USD')
        self.assertFalse(TickerRenderer.market_status_closed(crypto))

    def test_market_status_closed_2(self):
        stock = Stock('TSLA', 'USD')
        self.assertIsInstance(TickerRenderer.market_status_closed(stock), bool)
