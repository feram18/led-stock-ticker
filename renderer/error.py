from rgbmatrix import graphics
from utils import load_font, load_color, align_center, align_center_vertically


class ErrorRenderer:
    """
    Render an error message

    Properties:
        matrix           RGBMatrix instance
        canvas           Canvas associated with matrix
        config           Config instance
        error_msg        String containing error information
    """
    def __init__(self, matrix, canvas, config, error_msg: str):
        self.matrix = matrix
        self.canvas = canvas
        self.error_msg = error_msg

        # Load Font
        self.FONT_4X6 = config.layout["fonts"]["4x6"]
        self.font = load_font(self.FONT_4X6["path"])

        # Load text color
        self.text_color = load_color(config.colors["error"])

        # Set coords
        self.error_x = align_center(error_msg, matrix.width / 2, self.FONT_4X6["width"])
        self.error_y = align_center_vertically(matrix.height / 2, self.FONT_4X6["height"])

    def render(self):
        self.canvas.Clear()
        self.__render_error_msg()
        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def __render_error_msg(self):
        return graphics.DrawText(self.canvas, self.font, self.error_x, self.error_y, self.text_color, self.error_msg)
