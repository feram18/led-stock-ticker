"""Constants class"""

# Directories & Files
CONFIG_FILE = 'matrix/config.json'
CONFIG_SCHEMA = 'matrix/config.schema.json'
LAYOUT_FILE = 'matrix/coords/w{}h{}.json'
LOG_FILE = 'led-stock-ticker.log'
LOADING_IMAGE = 'assets/img/logo.png'
ERROR_IMAGE = 'assets/img/error.png'
FONTS_DIR = 'assets/fonts/'

# Software Defaults
DEFAULT_STOCKS = [
    'TSLA'
]
DEFAULT_CRYPTOS = [
    'BTC',
    'ETH',
    'VET',
    'KLV'
]
DEFAULT_FOREX = [
    
]
DEFAULT_CURRENCY = 'USD'
DEFAULT_DATE_FORMAT = '%a, %b %d'  # eg. Sun, Jan 5
DEFAULT_UPDATE_RATE = 5 * 60  # 5 minutes
DEFAULT_ROTATION_RATE = 10  # seconds
TEXT_SCROLL_DELAY = 0.5  # seconds
TEXT_SCROLL_SPEED = 0.3  # seconds

# Exchange Rate API
CURRENCY_EXCHANGE_URL = 'https://open.er-api.com/v6/latest/USD'

# Image sources
STOCK_LOGO_URL = 'https://logo.clearbit.com/{}'
CRYPTO_LOGO_URL = 'https://coinicons-api.vercel.app/api/icon/{}'
FLAG_URL = 'https://raw.githubusercontent.com/vivekimsit/currency-flags/master/src/flags/{}.png'

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
