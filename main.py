from rgbmatrix import RGBMatrix, RGBMatrixOptions
from data.matrix_config import MatrixConfig
from utils import args, led_matrix_options
from renderer.main import MainRenderer
from renderer.loading import Loading
from data.data import Data
import debug

SCRIPT_NAME = "LED-Stock-Ticker"
SCRIPT_VERSION = "0.0.1"

# Get CLI arguments
args = args()

# Check for LED configuration arguments
matrixOptions = led_matrix_options(args)

# Initialize the matrix
matrix = RGBMatrix(options=matrixOptions)

# Print some basic info on startup
debug.info("{} - v{} ({}x{})".format(SCRIPT_NAME, SCRIPT_VERSION, matrix.width, matrix.height))

# Read scoreboard options from config.json if it exists
config = MatrixConfig(matrix.width, matrix.height)
debug.set_debug_status(config)

# Display loading screen
Loading(matrix, config).render()

# Fetch initial data
data = Data(config)

MainRenderer(matrix, data).render()
