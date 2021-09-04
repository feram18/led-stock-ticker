import sys
import logging
from rgbmatrix import RGBMatrix
from constants import SCRIPT_NAME
from utils import args, led_matrix_options
from version import __version__
from config.config import Config
from data.data import Data
from renderer.main import MainRenderer
from renderer.loading import Loading


def main(matrix_):
    # Print script details on startup
    print(f'\U0001F4CA {SCRIPT_NAME} - v{__version__} ({matrix_.width}x{matrix_.height})')

    # Read software preferences from config.json
    config = Config(matrix_.width, matrix_.height)

    # Render loading splash screen
    Loading(matrix_, config).render()

    # Fetch initial data
    data = Data(config)

    # Begin rendering screen rotation
    MainRenderer(matrix_, data).render()


if __name__ == '__main__':
    # Get logging level
    if '--debug' in sys.argv:
        log_level = logging.DEBUG
        sys.argv.remove('--debug')
    else:
        log_level = logging.WARNING

    # Set logger configuration
    logging.basicConfig(filename='led-stock-ticker.log',
                        filemode='w',
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=log_level)

    # Check for led configuration arguments
    matrixOptions = led_matrix_options(args())

    # Initialize the matrix
    matrix = RGBMatrix(options=matrixOptions)

    try:
        main(matrix)
    except Exception as e:
        logging.exception(SystemExit(e))
    finally:
        matrix.Clear()
