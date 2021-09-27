import pytest
import sys
from data.crypto import Crypto


@pytest.mark.skipif(not sys.platform.startswith('linux'), reason='Requires Linux')
class TestCrypto:
    def setup_method(self):
        self.crypto = Crypto('ETH-USD', 'USD')

    def teardown_method(self):
        del self.crypto

    def test_get_name(self):
        name = self.crypto.get_name()
        assert name == 'Ethereum'
