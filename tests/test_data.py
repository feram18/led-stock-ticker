import pytest
import time
from api.data import Data
from config.matrix_config import MatrixConfig
from constants import DEFAULT_UPDATE_RATE


class TestData:
    def setup_method(self):
        self.data = Data(MatrixConfig(64, 32))

    def teardown_method(self):
        del self.data

    @pytest.mark.slow
    def test_should_update(self):
        time.sleep(DEFAULT_UPDATE_RATE)
        assert self.data.should_update() is True

    def test_should_update_2(self):
        assert self.data.should_update() is False
