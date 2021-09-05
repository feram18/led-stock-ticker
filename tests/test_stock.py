from unittest import TestCase
from data.stock import Stock
from PIL.Image import Image


class TestStock(TestCase):
    def setUp(self) -> None:
        self.stock = Stock('VZ', 'EUR')

    def test_get_logo(self):
        logo = self.stock.get_logo()
        self.assertIsInstance(logo, Image)
