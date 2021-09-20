import sys
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
from rgbmatrix import RGBMatrix
from utils import args, led_matrix_options
from version import __version__
from config.matrix_config import MatrixConfig
from data.data import Data
from renderer.main import MainRenderer
from renderer.loading import Loading


def main(matrix_):
    # Print script details on startup
    print(f'\U0001F4CA LED-Stock-Ticker - v{__version__} ({matrix_.width}x{matrix_.height})')

    # Read software preferences from config.json
    config = MatrixConfig(matrix_.width, matrix_.height)

    # Render loading splash screen
    Loading(matrix_, config).render()

    # Fetch initial data
    data = Data(config)

    # Begin rendering screen rotation
    MainRenderer(matrix_, data).render()


if __name__ == '__main__':
    # Get logging level
    if '--debug' in sys.argv:
        LOG_LEVEL = logging.DEBUG
        sys.argv.remove('--debug')
    else:
        LOG_LEVEL = logging.WARNING

    # Set logger configuration
    logger = logging.getLogger('')
    logger.setLevel(LOG_LEVEL)
    handler = RotatingFileHandler(filename='led-stock-ticker.log',
                                  maxBytes=5 * 1024 * 1024,
                                  backupCount=5)
    handler.setFormatter(Formatter(fmt='%(asctime)s %(levelname)s: %(message)s',
                                   datefmt='%m/%d/%Y %I:%M:%S %p'))
    logger.addHandler(handler)

    # Check for led configuration arguments
    matrixOptions = led_matrix_options(args())

    # Initialize the matrix
    matrix = RGBMatrix(options=matrixOptions)

    try:
        main(matrix)
    except Exception as e:  # For any random unhandled exceptions
        logging.exception(SystemExit(e))
    finally:
        matrix.Clear()
