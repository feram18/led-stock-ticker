import time

import pytest

from api.data import Data
from config.matrix_config import MatrixConfig


class TestData:
    def setup_method(self):
        self.data = Data(MatrixConfig(64, 32))

    def teardown_method(self):
        del self.data

    @pytest.mark.slow
    def test_should_update(self):
        time.sleep(self.data.config.update_rate)
        assert self.data.should_update() is True

    def test_should_update_2(self):
        assert self.data.should_update() is False
