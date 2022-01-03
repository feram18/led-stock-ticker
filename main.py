import sys
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
from rgbmatrix import RGBMatrix
from utils import args, led_matrix_options
from version import __version__
from config.matrix_config import MatrixConfig
from api.data import Data
from renderer.main import MainRenderer
from renderer.loading import Loading


def main():
    # Print script details on startup
    print(f'\U0001F4CA LED-Stock-Ticker - v{__version__} ({matrix.width}x{matrix.height})')

    # Read software preferences from config.json
    config = MatrixConfig(matrix.width, matrix.height)

    # Create canvas
    canvas = matrix.CreateFrameCanvas()

    # Render loading splash screen
    Loading(matrix, canvas, config).render()

    # Fetch initial data
    data = Data(config)

    # Begin rendering screen rotation
    MainRenderer(matrix, canvas, config, data).render()


if __name__ == '__main__':
    # Get logging level
    if '--debug' in sys.argv:
        LOG_LEVEL = logging.DEBUG
        sys.argv.remove('--debug')
    else:
        LOG_LEVEL = logging.WARNING

    # Set logger configuration
    logger = logging.getLogger('')  # root logger
    logger.setLevel(LOG_LEVEL)
    handler = RotatingFileHandler(filename='led-stock-ticker.log',
                                  maxBytes=5 * 1024 * 1024,  # 5MB
                                  backupCount=4)
    handler.setFormatter(Formatter(fmt='%(asctime)s %(levelname)s: %(message)s',
                                   datefmt='%m/%d/%Y %I:%M:%S %p'))
    logger.addHandler(handler)

    # Initialize the matrix
    matrix = RGBMatrix(options=led_matrix_options(args()))

    try:
        main()
    except Exception as e:  # For any random unhandled exceptions
        logging.exception(SystemExit(e))
    finally:
        matrix.Clear()
