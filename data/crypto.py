from dataclasses import dataclass

from data.ticker import Ticker


@dataclass
class Crypto(Ticker):
    img_url: str = None

    def initialize(self):
        super(Crypto, self).initialize()
        self.name = self.name.replace(' USD', '')
        self.img_url = self.price_data.get('logoUrl')
