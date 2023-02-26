import logging
from dataclasses import dataclass

from data.quote import QuoteType
from data.ticker import Ticker
from constants import STOCK_LOGO_URL


@dataclass
class Stock(Ticker):
    logo_url: str = None

    def initialize(self):
        super(Stock, self).initialize()
        if self.quote.get('quoteType') == QuoteType.EQUITY.name:
            self.logo_url = STOCK_LOGO_URL.format(self.yq_ticker.summary_profile
                                                  .get(self.symbol.upper())
                                                  .get('website'))
        else:
            logging.warning(f'Unable to get logo for {self.symbol}.')
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
