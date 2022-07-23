import sys
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
from rgbmatrix import RGBMatrix
from constants import LOG_FILE
from util.utils import args, led_matrix_options
from version import __version__
from config.matrix_config import MatrixConfig
from api.data import Data
from renderer.main import MainRenderer
from renderer.loading import Loading


def main():
    print(f'\U0001F4CA LED-Stock-Ticker - v{__version__} ({matrix.width}x{matrix.height})')

    config = MatrixConfig(matrix.width, matrix.height)

    canvas = matrix.CreateFrameCanvas()

    Loading(matrix, canvas, config).render()

    data = Data(config)

    MainRenderer(matrix, canvas, config, data).render()


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

    try:
        main()
    except Exception as e:
        logging.exception(SystemExit(e))
    finally:
        matrix.Clear()
