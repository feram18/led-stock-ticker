import pytest
import sys
from PIL.Image import Image
from data.stock import Stock


@pytest.mark.skipif(not sys.platform.startswith('linux'), reason='Requires Linux')
class TestStock:
    def setup_method(self):
        self.stock = Stock('VZ', 'EUR')

    def teardown_method(self):
        del self.stock

    def test_get_logo(self):
        logo = self.stock.get_logo()
        assert isinstance(logo, Image)
