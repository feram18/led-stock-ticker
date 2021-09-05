from unittest import TestCase
from PIL.Image import Image
from data.stock import Stock


class TestStock(TestCase):
    def setUp(self) -> None:
        self.stock = Stock('VZ', 'EUR')

    def test_get_logo(self):
        logo = self.stock.get_logo()
        self.assertIsInstance(logo, Image)
