import pytest
import sys
from renderer.ticker import TickerRenderer
from util.color import Color


@pytest.mark.skipif(not sys.platform.startswith('linux'), reason='Requires Linux')
class TestTickerRenderer:
    def test_format_price(self):
        result = TickerRenderer.format_price('USD', 78.23)
        assert result == '$78.23'

    def test_format_price_2(self):
        result = TickerRenderer.format_price('PLN', 78.23)
        assert result == 'zł78.23'

    def test_set_change_color(self):
        color = TickerRenderer.set_change_color(78.23)
        assert color == Color.GREEN

    def test_set_change_color_2(self):
        color = TickerRenderer.set_change_color(-14.68)
        assert color == Color.RED

    def test_set_change_color_3(self):
        color = TickerRenderer.set_change_color(0)
        assert color == Color.GREEN
