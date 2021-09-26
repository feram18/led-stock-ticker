import unittest
import sys
from unittest import TestCase
from renderer.crypto import CryptoRenderer


@unittest.skipUnless(sys.platform.startswith("linux"), "Requires Linux")
class TestCryptoRenderer(TestCase):
    def test_format_symbol(self):
        result = CryptoRenderer.format_symbol('BTC-USD')
        self.assertEqual(result, 'BTC')

    def test_format_symbol_2(self):
        result = CryptoRenderer.format_symbol('BTC')
        self.assertEqual(result, 'BTC')
