from rgbmatrix import RGBMatrixOptions, graphics
from constants import DEFAULT_FONT_PATH
import argparse
import logging
import json
import os


def get_file(path: str) -> str:
    """
    Read file
    :param path: str
    :return: abs_file_path: str
    """
    dir = os.path.dirname(__file__)
    return os.path.join(dir, path)


def read_json(filename: str) -> dict:
    """
    Read JSON file, and return JSON object.
    :param filename: str
    :return: j: dict
    """
    j = {}
    path = get_file(filename)
    if os.path.isfile(path):
        j = json.load(open(path))
    return j


def text_offscreen(text: str, canvas_width: int, font_width: int) -> bool:
    """
    Determines if text will go off-screen
    :param text: str
    :param canvas_width: int
    :param font_width: int
    :return: offscreen: boolean
    """
    return len(text) > canvas_width / font_width


def align_center(text: str, center_pos: int, font_width: int) -> int:
    """
    Calculate x-coord to align text to center of matrix
    :param text: str
    :param center_pos: int
    :param font_width: int
    :return: x_coord: int
    """
    return abs(center_pos - (len(text) * font_width) // 2)


def align_right(text: str, right_limit: int, font_width: int) -> int:
    """
    Calculates x-coord to align text to right of matrix
    :param text: str
    :param right_limit: int
    :param font_width: int
    :return: x_coord: int
    """
    return abs(right_limit - (len(text) * font_width))


def align_center_vertically(center_pos: int, font_height: int) -> int:
    """
    Returns y-coord to align text to center of matrix
    :param center_pos: int
    :param font_height: int
    :return: y_coord: int
    """
    return abs(center_pos + font_height // 2)


def load_color(colors: dict):
    """
    Convert RGB values from JSON into Color object
    :param colors: JSON
    :return: color: Color
    """
    try:
        return graphics.Color(colors["r"], colors["g"], colors["b"])
    except ValueError:
        logging.warning("Could not read colors. Setting color to default White")
        return graphics.Color(255, 255, 255)


def load_font(path: str):
    """
    Return Font object from given path
    :param path: str
    :return: font: Font
    """
    font = graphics.Font()
    try:
        font.LoadFont(path)
    except FileNotFoundError:
        logging.warning(f"Could not load font at {path}. Setting font to default 4x6")
        font.LoadFont(DEFAULT_FONT_PATH)
    return font


def args():
    """
    Parse command line arguments to configure matrix
    :return: parsed_arguments: ArgumentParser
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--led-rows",
                        action="store",
                        help="Display rows. 16 for 16x32, 32 for 32x32. (Default: 32)",
                        default=32,
                        type=int)
    parser.add_argument("--led-cols",
                        action="store",
                        help="Panel columns. Typically 32 or 64. (Default: 32)",
                        default=32,
                        type=int)
    parser.add_argument("--led-chain",
                        action="store",
                        help="Daisy-chained boards. (Default: 1)",
                        default=1,
                        type=int)
    parser.add_argument("--led-parallel",
                        action="store",
                        help="For Plus-models or RPi2: parallel chains. 1..3. (Default: 1)",
                        default=1,
                        type=int)
    parser.add_argument("--led-pwm-bits",
                        action="store",
                        help="Bits used for PWM. Range 1..11. (Default: 11)",
                        default=11,
                        type=int)
    parser.add_argument("--led-brightness",
                        action="store",
                        help="Sets brightness level. Range: 1..100. (Default: 100)",
                        default=100,
                        type=int)
    parser.add_argument("--led-gpio-mapping",
                        help="Hardware Mapping: regular, adafruit-hat, adafruit-hat-pwm",
                        choices=['regular', 'adafruit-hat', 'adafruit-hat-pwm'],
                        type=str)
    parser.add_argument("--led-scan-mode",
                        action="store",
                        help="Progressive or interlaced scan. 0 = Progressive, 1 = Interlaced. (Default: 1)",
                        default=1,
                        choices=range(2),
                        type=int)
    parser.add_argument("--led-pwm-lsb-nanoseconds",
                        action="store",
                        help="Base time-unit for the on-time in the lowest significant bit in nanoseconds. "
                             "(Default: 130)",
                        default=130,
                        type=int)
    parser.add_argument("--led-show-refresh",
                        action="store_true",
                        help="Shows the current refresh rate of the LED panel.")
    parser.add_argument("--led-slowdown-gpio",
                        action="store",
                        help="Slow down writing to GPIO. Range: 0..4. (Default: 1)",
                        choices=range(5),
                        type=int)
    parser.add_argument("--led-no-hardware-pulse",
                        action="store",
                        help="Don't use hardware pin-pulse generation.")
    parser.add_argument("--led-rgb-sequence",
                        action="store",
                        help="Switch if your matrix has led colors swapped. (Default: RGB)",
                        default="RGB",
                        type=str)
    parser.add_argument("--led-pixel-mapper",
                        action="store",
                        help="Apply pixel mappers. e.g \"Rotate:90\"",
                        default="",
                        type=str)
    parser.add_argument("--led-row-addr-type",
                        action="store",
                        help="0 = default; 1 = AB-addressed panels; 2 = direct row select; "
                             "3 = ABC-addressed panels. (Default: 0)",
                        default=0,
                        type=int,
                        choices=[0, 1, 2, 3])
    parser.add_argument("--led-multiplexing",
                        action="store",
                        help="Multiplexing type: 0 = direct; 1 = strip; 2 = checker; 3 = spiral; 4 = Z-strip; "
                             "5 = ZnMirrorZStripe; 6 = coreman; 7 = Kaler2Scan; 8 = ZStripeUneven. (Default: 0)",
                        default=0,
                        type=int)

    return parser.parse_args()


def led_matrix_options(args):
    """
    Set RGB LED matrix options from parsed arguments
    :param args: ArgumentParser
    :return: options: RGBMatrixOptions
    """
    options = RGBMatrixOptions()

    if args.led_gpio_mapping is not None:
        options.hardware_mapping = args.led_gpio_mapping

    options.rows = args.led_rows
    options.cols = args.led_cols
    options.chain_length = args.led_chain
    options.parallel = args.led_parallel
    options.row_address_type = args.led_row_addr_type
    options.multiplexing = args.led_multiplexing
    options.pwm_bits = args.led_pwm_bits
    options.brightness = args.led_brightness
    options.pwm_lsb_nanoseconds = args.led_pwm_lsb_nanoseconds
    options.led_rgb_sequence = args.led_rgb_sequence
    try:
        options.pixel_mapper_config = args.led_pixel_mapper
    except AttributeError:
        logging.warning("Your compiled RGB Matrix Library is out of date.")
        logging.warning("The --led-pixel-mapper argument will not work until it is updated.")

    if args.led_show_refresh:
        options.show_refresh_rate = 1

    if args.led_slowdown_gpio is not None:
        options.gpio_slowdown = args.led_slowdown_gpio

    if args.led_no_hardware_pulse:
        options.disable_hardware_pulsing = True

    return options
