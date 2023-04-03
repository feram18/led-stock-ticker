"""Class with miscellaneous utility functions"""
import argparse
import json
import logging
import operator
import os
from datetime import datetime
from io import BytesIO
from typing import Tuple, List

import requests
from PIL import Image, ImageFont, UnidentifiedImageError
from rgbmatrix import RGBMatrixOptions
from pytz import timezone
from requests import Timeout, RequestException, ConnectionError

import constants
from util.market_status import MarketStatus
from util.color import Color
from util.holiday_calendar import MarketHolidayCalendar
from util.position import Position
from util.retry import retry


def read_json(filename: str) -> dict:
    """
    Read from JSON file and return it as a dictionary
    :param filename: (str) JSON file
    :return: json: (dict) JSON file as a dict
    """
    if os.path.isfile(filename):
        with open(filename, 'r') as json_file:
            logging.debug(f'Reading JSON file at {filename}')
            return json.load(json_file)
    logging.error(f"Couldn't find file at {filename}")


def write_json(filename: str, data: dict):
    """
    Write to JSON file from dictionary.
    :param filename: (str) file to write dictionary to
    :param data: (dict) dictionary to write to file
    """
    with open(filename, 'w') as json_file:
        logging.debug(f'Writing JSON to file at {filename}')
        json.dump(data, json_file, indent=4)


def off_screen(canvas_width: int, text_size: int) -> bool:
    """
    Determines if text will go off-screen
    :param canvas_width: (int) Canvas width
    :param text_size: (int) Text size in pixels
    :return: off-screen: (bool)
    """
    return text_size > canvas_width


def align_text(text_size: Tuple[int, int],
               col_width: int = 0,
               col_height: int = 0,
               x: Position = Position.CENTER,
               y: Position = Position.CENTER) -> Tuple[int, int]:
    """
    Calculate x, y coords to align text on canvas
    :param text_size: (width, height) in pixels
    :param x: Text's horizontal position
    :param y: Text's vertical position
    :param col_width: Column's width
    :param col_height: Column's height
    :return: x, y: Coordinates
    """
    if x == Position.RIGHT:
        x = col_width - text_size[0]
    elif x == Position.CENTER:
        x = abs(col_width//2 - text_size[0]//2)
    elif x == Position.LEFT:
        x = 0

    if y == Position.CENTER:
        y = abs(col_height//2 - text_size[1]//2)
    elif y == Position.BOTTOM:
        y = col_height - text_size[1]
    elif y == Position.TOP:
        y = 0

    return x, y


def align_image(image: Image,
                col_width: int = 0,
                col_height: int = 0,
                x: Position = Position.CENTER,
                y: Position = Position.CENTER) -> Tuple[int, int]:
    """
    Calculate the x, y offsets to align image on canvas
    :param image: Image to align
    :param col_width: Column's width
    :param col_height: Column's height
    :param x: Image horizontal position
    :param y: Image vertical position
    :return: x, y: Coordinates
    """
    if x == Position.RIGHT:
        x = col_width - image.width
    elif x == Position.CENTER:
        x = abs(col_width//2 - image.width//2)
    elif x == Position.LEFT:
        x = 0

    if y == Position.CENTER:
        y = abs(col_height//2 - image.height//2)
    elif y == Position.BOTTOM:
        y = col_height - image.height
    elif y == Position.TOP:
        y = 0

    return x, y


def load_font(filename: str, size: int) -> ImageFont:
    """
    Return ImageFont object from given font name
    :param filename: Font filename
    :param size: Font size
    :return: font: ImageFont object
    """
    path = constants.FONTS_DIR + filename
    if os.path.isfile(path):
        return ImageFont.truetype(path, size)
    logging.error(f"Couldn't find font {path}.")


def load_image(filename: str,
               size: Tuple[int, int],
               background: tuple = Color.BLACK) -> Image:
    """
    Open Image file from given path
    :param filename: Path to the image file
    :param size: Maximum width and height of the image
    :param background: Background color for PNG images
    :return: image: Image file
    """
    if filename and os.path.isfile(filename):
        with Image.open(filename) as original:
            if '.png' in filename:
                original = original.crop(original.getbbox())  # Non-empty pixels
                image = Image.new('RGB',  # Background img
                                  (original.width, original.height),
                                  background)
                image.paste(original)  # Paste original on background
                image.thumbnail(size)  # Resize
                return image
            else:  # Non-transparent images
                original.thumbnail(size)
                return original.convert('RGB')
    logging.error(f"Couldn't find image {filename}")


def load_image_url(url: str, size: Tuple[int, int]) -> Image:
    """
    Fetch the stock's company logo.
    :param url: URL to logo image
    :param size: Image size
    :return: image: Image from URL
    :exception UnidentifiedImageError: If image cannot be opened/identified
    :exception ConnectionError: If connection error occurred
    """
    if url:
        response = requests.get(url)
        if response.ok:
            try:
                with Image.open(BytesIO(response.content)) as img:
                    img.thumbnail(size)
                    return img.convert('RGB')
            except UnidentifiedImageError:
                logging.error(f'Could not get image at {url}')
    else:
        logging.error('No url provided')


def build_forex_img(urls: List[str], size: Tuple[int, int]) -> Image:
    """
    Build image with flags of forex pair countries
    :param urls: URLs to country flags
    :param size: image size
    :return: image: Image with flag of currency from/to
    """
    img = Image.new('RGB', size)
    flag_size = round(0.67 * size[0])
    flag_from = load_image_url(urls[0], (flag_size, flag_size))
    flag_to = load_image_url(urls[1], (flag_size, flag_size))

    if flag_from and flag_to:
        img.paste(flag_from)
        img.paste(flag_to, tuple(map(operator.sub, size, flag_to.size)))
        return img
    logging.warning('Unable to build forex image')


@retry((Timeout, ConnectionError), total_tries=3)
def convert_currency(currency_from: str, currency_to: str, amount: float) -> float:
    """
    Convert a value from one currency to another.
    :param currency_from: (str) Currency to convert from
    :param currency_to: (str) Currency to convert to
    :param amount: (float) Amount to convert
    :return: result: (float) Converted amount
    :exception TypeError: If incorrect data type is provided as an argument
    :exception Timeout: If the request timed out
    :exception ConnectionError: If a connection error occurred
    :exception RequestException: If an ambiguous exception that occurred
    """
    try:
        url = constants.CURRENCY_EXCHANGE_URL.format(currency_from, currency_to, amount)
        response = requests.get(url).json()
        return float(response['result'])
    except TypeError:
        return 0.0
    except RequestException:
        logging.error('Encountered an unknown error while converting currency. Returning original value.')
        return amount


def market_status() -> MarketStatus:
    """
    Determine if the stock market is closed.
    :return: market_closed: (MarketStatus)
    """
    return MarketStatus.CLOSED if holiday() or after_hours() else MarketStatus.OPEN


def after_hours() -> bool:
    """
    Determine if current time is after hours.
    i.e. Current time is not between 09:30 AM and 04:00 PM EST (Regular stock market hours), or it is a weekend.
    :return: after_hours: (bool)
    """
    current_time = datetime.now(timezone('US/Eastern'))  # Current time in EST
    open_market = current_time.replace(hour=9, minute=30, second=0, microsecond=0)  # 09:30 AM EST
    close_market = current_time.replace(hour=16, minute=0, second=0, microsecond=0)  # 04:00 PM EST
    return current_time < open_market or current_time > close_market or weekend()


def weekend() -> bool:
    """
    Determine if today is a weekend day.
    :return: weekend: (bool)
    """
    week_day_no = datetime.today().weekday()
    return week_day_no > 4  # 5 Sat, 6 Sun


def holiday() -> bool:
    """
    Determine if today is an NYSE-observed US federal holiday.
    :return: holiday: (bool)
    """
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    sdt = today.replace(month=1, day=1)  # Year start-date
    edt = today.replace(month=12, day=31)  # Year end-date
    holidays = MarketHolidayCalendar().holidays(start=sdt, end=edt).to_pydatetime()
    return today in holidays


def args() -> argparse.Namespace:
    """
    CLI argument parser to configure matrix.
    :return: parser: (argsparse.Namespace) Argument parser
    """
    parser = argparse.ArgumentParser(prog='LED-Stock-Ticker')

    parser.add_argument('--led-rows',
                        action='store',
                        help='Display rows. 16 for 16x32, 32 for 32x64, etc. (Default: 32)',
                        type=int,
                        default=32)
    parser.add_argument('--led-cols',
                        action='store',
                        help='Display columns. 32 for 16x32, 64 for 32x62, etc. (Default: 64)',
                        type=int,
                        default=64)
    parser.add_argument('--led-multiplexing',
                        action='store',
                        help='Multiplexing type: 0 = direct; 1 = strip; 2 = checker; 3 = spiral; 4 = Z-strip; '
                             '5 = ZnMirrorZStripe; 6 = coreman; 7 = Kaler2Scan; 8 = ZStripeUneven. (Default: 0)',
                        type=int,
                        choices=range(9),
                        default=0)
    parser.add_argument('--led-row-addr-type',
                        action='store',
                        help='Addressing of rows: 0 = default; 1 = AB-addressed panels; 2 = direct row select; '
                             '3 = ABC-addressed panels. (Default: 0)',
                        type=int,
                        choices=range(4),
                        default=0)
    parser.add_argument('--led-panel-type',
                        action='store',
                        help='Chipset of the panel. Supported panel types: FM6126A; FM6127.',
                        type=str,
                        choices=['FM6126A', 'FM6127'],
                        default='')
    parser.add_argument('--led-gpio-mapping',
                        help='Name of GPIO mapping used: regular, adafruit-hat, adafruit-hat-pwm, compute-module',
                        type=str,
                        choices=['regular', 'adafruit-hat', 'adafruit-hat-pwm', 'compute-module'],
                        default='regular')
    parser.add_argument('--led-slowdown-gpio',
                        action='store',
                        help="Slow down writing to GPIO. Needed for faster Pi's and/or slower panels. Range: 0..4. "
                             '(Default: 1)',
                        type=int,
                        choices=range(5),
                        default=1)
    parser.add_argument('--led-chain',
                        action='store',
                        help='Number of daisy-chained boards. (Default: 1)',
                        type=int,
                        default=1)
    parser.add_argument('--led-parallel',
                        action='store',
                        help='For Plus-models or RPi2: parallel chains. 1..3. (Default: 1)',
                        type=int,
                        default=1)
    parser.add_argument('--led-pixel-mapper',
                        action='store',
                        help='Apply pixel mappers: '
                             'Mirror (Horizontal) = \"Mirror:H\"; '
                             'Mirror (Vertical) = \"Mirror:V\"; '
                             'Rotate (Degrees) = eg. \"Rotate: 90\"; '
                             'U-Mapper = \"U-mapper\"',
                        type=str,
                        default='')
    parser.add_argument('--led-brightness',
                        action='store',
                        help='Brightness level. Range: 1..100. (Default: 100)',
                        type=int,
                        choices=range(101),
                        default=100)
    parser.add_argument('--led-pwm-bits',
                        action='store',
                        help='Bits used for PWM. Range 1..11. (Default: 11)',
                        type=int,
                        choices=range(12),
                        default=11)
    parser.add_argument('--led-show-refresh',
                        action='store_true',
                        help='Shows the current refresh rate of the LED panel.')
    parser.add_argument('--led-limit-refresh',
                        action='store',
                        help='Limit refresh rate to this frequency in Hz. Useful to keep a constant refresh rate on '
                             'loaded system. 0=no limit. (Default: 0)',
                        type=int,
                        default=0)
    parser.add_argument('--led-scan-mode',
                        action='store',
                        help='Progressive or interlaced scan. 0 = Progressive, 1 = Interlaced. (Default: 1)',
                        type=int,
                        choices=range(2),
                        default=1)
    parser.add_argument('--led-pwm-lsb-nanoseconds',
                        action='store',
                        help='Base time-unit for the on-time in the lowest significant bit in nanoseconds. '
                             '(Default: 130)',
                        type=int,
                        default=130)
    parser.add_argument('--led-pwm-dither-bits',
                        action='store',
                        help='Time dithering of lower bits (Default: 0)',
                        type=int,
                        default=0)
    parser.add_argument('--led-no-hardware-pulse',
                        action='store',
                        help="Don't use hardware pin-pulse generation.")
    parser.add_argument('--led-inverse',
                        action='store',
                        help='Switch if your matrix has inverse colors on.')
    parser.add_argument('--led-rgb-sequence',
                        action='store',
                        help='Switch if your matrix has led colors swapped. (Default: RGB)',
                        type=str,
                        default='RGB')

    return parser.parse_args()


def led_matrix_options(args_: argparse.Namespace) -> RGBMatrixOptions:
    """
    Set RGBMatrixOptions from parsed arguments.
    :param args_: (argsparse.Namespace) Parsed arguments from CLI
    :return: options: (rgbmatrix.RGBMatrixOptions) RGBMatrixOptions instance
    :exception AttributeError: If attribute is not found
    """
    options = RGBMatrixOptions()

    options.rows = args_.led_rows
    options.cols = args_.led_cols
    options.multiplexing = args_.led_multiplexing
    options.row_address_type = args_.led_row_addr_type

    if args_.led_panel_type is not None:
        options.panel_type = args_.led_panel_type

    if args_.led_gpio_mapping is not None:
        options.hardware_mapping = args_.led_gpio_mapping

    if args_.led_slowdown_gpio is not None:
        options.gpio_slowdown = args_.led_slowdown_gpio

    options.chain_length = args_.led_chain
    options.parallel = args_.led_parallel
    options.pixel_mapper_config = args_.led_pixel_mapper
    options.brightness = args_.led_brightness
    options.pwm_bits = args_.led_pwm_bits

    if args_.led_show_refresh:
        options.show_refresh_rate = 1

    options.limit_refresh_rate_hz = args_.led_limit_refresh
    options.scan_mode = args_.led_scan_mode
    options.pwm_lsb_nanoseconds = args_.led_pwm_lsb_nanoseconds
    options.pwm_dither_bits = args_.led_pwm_dither_bits

    if args_.led_no_hardware_pulse:
        options.disable_hardware_pulsing = True

    if args_.led_inverse:
        options.inverse_colors = args_.led_inverse

    options.led_rgb_sequence = args_.led_rgb_sequence

    return options
