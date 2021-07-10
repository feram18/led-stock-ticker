# Directories & Files
CONFIG_FILE = "config/config.json"
COLORS_FILE = "config/colors.json"
LAYOUT_FILE = "config/layout/w{}h{}.json"

# Defaults
DEFAULT_TICKERS = ["TSLA", "AMZN", "AAPL", "MSFT"]
DEFAULT_COUNTRY = "US"
DEFAULT_CURRENCY = "USD"
DEFAULT_TIMEZONE = "EST"
DEFAULT_TIME_FORMAT = "12h"
EASTERN_TZ = "US/Eastern"

# API & Requests
BASE_URL = "https://api.twelvedata.com/{}"
PREVIOUS_DAY_CLOSE_PRICE_URL = BASE_URL\
    .format("time_series?symbol={}&interval={}&outputsize={}&dp={}&previous_close={}&apikey={}")
CURRENT_PRICE_URL = BASE_URL.format("price?symbol={}&dp={}&apikey={}")
STOCK_NAME_URL = BASE_URL.format("stocks?symbol={}&country={}")
CRYPTO_NAME_URL = BASE_URL.format("cryptocurrencies?symbol={}")
SYMBOL_SEARCH_URL = BASE_URL.format("symbol_search?symbol={}")
MAX_API_REQUESTS = 800
DECIMAL_PLACES = 2
INTERVAL = "1day"
OUTPUT_SIZE = 1

# Date/Time Formatting
DATE_FORMAT = "%a, %B %d"  # eg. Sun, June 5
TWELVE_HOURS_DATE_FORMAT = "%I:%M %p"  # eg. 11:38 PM
TWENTY_FOUR_HOURS_DATE_FORMAT = "%H:%M"  # eg. 23:38

# Software
SCRIPT_NAME = "LED-Stock-Ticker"
SCRIPT_VERSION = "v0.0.1"
ROTATION_RATE = 15.0  # 15 seconds
REFRESH_DELAY = 5.0  # 5 seconds
TEXT_SCROLL_DELAY = 0.5
TEXT_SCROLL_SPEED = 0.1
NETWORK_RETRY = 60.0  # 60 seconds

# Error
ERROR_STR = "ERROR"
NETWORK_ERROR = "Network Error"
API_ERROR = "API Error"

# Misc
LOADING_STR = "LOADING"
