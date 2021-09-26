import unittest
import sys
from unittest import TestCase
from renderer.ticker import TickerRenderer
from data.color import Color


@unittest.skipUnless(sys.platform.startswith("linux"), "Requires Linux")
class TestTickerRenderer(TestCase):
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
