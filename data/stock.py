import logging
from dataclasses import dataclass

from data.quote import QuoteType
from data.status import Status
from data.ticker import Ticker
from constants import STOCK_LOGO_URL
from util.market_status import MarketStatus


@dataclass
class Stock(Ticker):
    market_status: MarketStatus = MarketStatus.OPEN
    logo_url: str = None

    def initialize(self):
        super(Stock, self).initialize()
        if self.price_data.get('quoteType') == QuoteType.EQUITY.name:
            self.logo_url = STOCK_LOGO_URL.format(self.yq_ticker.summary_profile
                                                  .get(self.symbol.upper())
                                                  .get('website'))
        else:
            logging.warning(f'Unable to get logo for {self.symbol}.')
        self.market_status = MarketStatus.OPEN if self.price_data.get('marketState') == 'REGULAR' \
            else MarketStatus.CLOSED
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
        
    def update(self) -> Status:
        super(Stock, self).update()
        self.market_status = MarketStatus.OPEN if self.price_data.get('marketState') == 'REGULAR' \
            else MarketStatus.CLOSED
        return Status.SUCCESS
