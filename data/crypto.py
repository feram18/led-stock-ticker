from dataclasses import dataclass

from constants import CRYPTO_LOGO_URL
from data.ticker import Ticker


@dataclass
class Crypto(Ticker):
    img_url: str = None

    def initialize(self):
        super(Crypto, self).initialize()
        self.name = self.name.replace(' USD', '')
        self.img_url = CRYPTO_LOGO_URL.format(self.symbol.replace('-USD', '').lower())
