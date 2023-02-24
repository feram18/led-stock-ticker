from dataclasses import dataclass

from data.ticker import Ticker
from constants import STOCK_LOGO_URL


@dataclass
class Stock(Ticker):
    logo_url: str = None

    def initialize(self):
        super(Stock, self).initialize()
        self.logo_url = STOCK_LOGO_URL.format(self.yq_ticker.summary_profile.get(self.symbol).get('website'))
        self.name = self.name\
            .replace('Company', '')\
            .replace('Corporation', '')\
            .replace('Holdings', '')\
            .replace('Incorporated', '')\
            .replace('Inc', '')\
            .replace('.com', '')\
            .replace('(The)', '') \
            .rstrip('& ')\
            .rstrip('. ')\
            .rstrip(', ')\
            .rstrip()
