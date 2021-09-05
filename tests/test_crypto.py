from unittest import TestCase
from data.crypto import Crypto


class TestCrypto(TestCase):
    def test_format_name(self):
        name = 'CRYPTO USD'
        formatted_name = Crypto.format_name(name)
        self.assertEqual(formatted_name, 'CRYPTO')

    def test_format_name_2(self):
        name = 'CRYPTO'
        formatted_name = Crypto.format_name(name)
        self.assertEqual(formatted_name, name)
