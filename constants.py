"""Constants class"""

# Directories & Files
CONFIG_FILE = 'config/config.json'
LAYOUT_FILE = 'config/layout/w{}h{}.json'
LOG_FILE = 'led-stock-ticker.log'
LOADING_IMAGE = 'assets/img/logo.png'
ERROR_IMAGE = 'assets/img/error.png'
FONTS_DIR = 'assets/fonts/'

# Software Defaults
DEFAULT_STOCKS = [
    'TSLA',
    'AMZN',
    'MSFT'
]
DEFAULT_CRYPTOS = [
    'BTC',
    'ETH',
    'LTC'
]
DEFAULT_FOREX = [
    'USD/EUR',
    'EUR/JPY',
    'GBP/USD'
]
DEFAULT_DATE_FORMAT = '%a, %b %d'  # eg. Sun, Jan 5
DEFAULT_UPDATE_RATE = 10 * 60  # 10 minutes
DEFAULT_ROTATION_RATE = 10  # seconds
TEXT_SCROLL_DELAY = 0.5  # seconds
TEXT_SCROLL_SPEED = 0.3  # seconds

# ExchangeRate API
EXCHANGE_RATE_BASE_URL = 'https://api.exchangerate.host/'
CURRENCY_EXCHANGE_URL = EXCHANGE_RATE_BASE_URL + 'convert?from={}&to={}&amount={}&places=2'
FOREX_RATES_URL = EXCHANGE_RATE_BASE_URL + 'fluctuation?start_date={}&end_date={}&base={}&symbols={}&places=4'

# Image sources
CRYPTO_LOGO_URL = 'https://cryptoicons.org/api/icon/{}/200'

# Date/Time Formatting
DATE_FORMATS = [
    '%a, %b %d',  # Sun, Jan 5
    '%B %d',  # January 5
    '%m/%d/%Y',  # MM/DD/YYYY
    '%a, %d %b',  # Sun, 5 Jan
    '%d/%m/%Y',  # DD/MM/YYYY
]
CLOCK_FORMATS = [
    '12h',
    '24h'
]
TWELVE_HOURS_FORMAT = '%I:%M %p'  # eg. 11:38 PM
TWENTY_FOUR_HOURS_FORMAT = '%H:%M'  # eg. 23:38
