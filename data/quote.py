from enum import Enum, auto


class QuoteType(Enum):
    EQUITY = auto()
    INDEX = auto()
    CRYPTOCURRENCY = auto()
    CURRENCY = auto()
    ETF = auto()
    MUTUALFUND = auto()
