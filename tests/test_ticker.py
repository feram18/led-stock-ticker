import pytest
import sys
import time
from data.ticker import Ticker
from constants import UPDATE_RATE


@pytest.mark.skipif(not sys.platform.startswith('linux'), reason='Requires Linux')
class TestTicker:
    def setup_method(self):
        self.ticker = Ticker('VZ', 'USD')

    def teardown_method(self):
        del self.ticker

    @pytest.mark.slow
    def test_should_update(self):
        time.sleep(UPDATE_RATE)
        assert self.ticker.should_update() is True
