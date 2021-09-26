import time
from rgbmatrix.graphics import DrawText
from renderer.renderer import Renderer
from utils import align_text_center, load_font, load_image
from constants import ERROR_IMAGE
from data.color import Color


class ErrorRenderer(Renderer):
    """
    Renderer for error messages

    Arguments:
        matrix (rgbmatrix.RGBMatrix):           RGBMatrix instance
        canvas (rgbmatrix.Canvas):              Canvas associated with matrix
        config (data.Config):                   Config instance
        error_msg (str):                        String containing error information

    Attributes:
        font (rgbmatrix.graphics.Font):         Font for error msg
        color (rgbmatrix.graphics.Color):       Color for error msg
        msg_x (int):                            Error msg's x-coord
        msg_y (int):                            Error msg's y-coord
    """

    def __init__(self, matrix, canvas, config, error_msg: str):
        super().__init__(matrix, canvas)
        self.error_msg = error_msg

        # Load font
        self.font = load_font(config.layout['fonts']['4x6'])

        # Load text color
        self.color = Color.RED

        # Load error image
        self.error_image = load_image(ERROR_IMAGE, (4, 6))

        # Set coords
        self.msg_x, self.msg_y = align_text_center(self.error_msg,
                                                   self.canvas.width,
                                                   self.canvas.height,
                                                   self.font.baseline - 1,
                                                   self.font.height)

        self.image_x_offset, self.image_y_offset = 0, 0

    def render(self):
        self.canvas.Clear()
        self.render_error_msg()
        time.sleep(5.0)
        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def render_error_msg(self):
        DrawText(self.canvas, self.font, self.msg_x, self.msg_y, self.color, self.error_msg)

    def render_image(self):
        self.canvas.SetImage(self.error_image, self.image_x_offset, self.image_y_offset)
