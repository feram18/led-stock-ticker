from dataclasses import dataclass, field
from typing import List

from constants import FLAG_URL
from data.ticker import Ticker


@dataclass
class Forex(Ticker):
    img_url: List[str] = field(init=False)

    def initialize(self):
        super(Forex, self).initialize()
        if self.valid:
            self.img_url = [FLAG_URL.format(i) for i in self.name.lower().split('/')]
