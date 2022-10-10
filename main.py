import sys
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter

from PIL import Image, ImageDraw
from rgbmatrix import RGBMatrix

from api.data import Data
from config.matrix_config import MatrixConfig
from constants import LOG_FILE
from renderer.loading import Loading
from renderer.main import MainRenderer
from util.utils import args, led_matrix_options
from version import __version__


def main():
    print(f'\U0001F4CA LED-Stock-Ticker - v{__version__} ({matrix.width}x{matrix.height})')
    config = MatrixConfig(matrix.width, matrix.height)
    Loading(matrix, canvas, draw, config)
    data = Data(config)
    MainRenderer(matrix, canvas, draw, config, data)


if __name__ == '__main__':
    if '--debug' in sys.argv:
        LOG_LEVEL = logging.DEBUG
        sys.argv.remove('--debug')
    else:
        LOG_LEVEL = logging.WARNING

    logger = logging.getLogger('')
    logger.setLevel(LOG_LEVEL)
    handler = RotatingFileHandler(filename=LOG_FILE,
                                  maxBytes=5 * 1024 * 1024,  # 5MB
                                  backupCount=4)
    handler.setFormatter(Formatter(fmt='%(asctime)s %(levelname)s: %(message)s',
                                   datefmt='%m/%d/%Y %I:%M:%S %p'))
    logger.addHandler(handler)

    matrix = RGBMatrix(options=led_matrix_options(args()))
    canvas = Image.new('RGB', (matrix.width, matrix.height))
    draw = ImageDraw.Draw(canvas)
    matrix.SetImage(canvas)

    try:
        main()
    except Exception as e:
        logging.exception(SystemExit(e))
    finally:
        matrix.Clear()
