"""Constants class"""

# Directories & Files
CONFIG_FILE = 'config/config.json'
LAYOUT_FILE = 'config/layout/w{}h{}.json'
LOADING_IMAGE = 'assets/img/logo.png'
ERROR_IMAGE = 'assets/img/error.png'

# Software Defaults
DEFAULT_STOCKS = ['TSLA', 'AMZN', 'MSFT']
DEFAULT_CRYPTOS = ['BTC', 'ETH', 'LTC']
CLOCK_FORMATS = ['12h', '24h']
DEFAULT_FONT_PATH = 'rpi-rgb-led-matrix/fonts/4x6.bdf'
DEFAULT_UPDATE_RATE = 10 * 60  # 10 minutes
DEFAULT_ROTATION_RATE = 10  # 10 seconds
TEXT_SCROLL_DELAY = 0.5  # 0.5 seconds
TEXT_SCROLL_SPEED = 0.1  # 0.1 seconds

# ExchangeRate API
CURRENCY_EXCHANGE_URL = 'https://api.exchangerate.host/convert?from={}&to={}&amount={}&places=2'

# Date/Time Formatting
DEFAULT_DATE_FORMAT = '%a, %b %d'  # eg. Sun, Jan 5
TWELVE_HOURS_FORMAT = '%I:%M %p'  # eg. 11:38 PM
TWENTY_FOUR_HOURS_FORMAT = '%H:%M'  # eg. 23:38
