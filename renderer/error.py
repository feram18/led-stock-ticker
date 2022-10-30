import time

from constants import ERROR_IMAGE
from renderer.renderer import Renderer
from util.color import Color
from util.position import Position
from util.utils import align_text, load_image, align_image


class ErrorRenderer(Renderer):
    """
    Renderer for error messages

    Arguments:
        data (api.Data):        Data instance

    Attributes:
        coords (dict):          Coordinates dictionary
        msg (str):              Error message string
    """

    def __init__(self, matrix, canvas, draw, config, data):
        super().__init__(matrix, canvas, draw, config)
        self.data = data
        self.coords: dict = self.config.layout.coords['error']
        self.msg: str = self.data.status

    def render(self):
        self.clear()
        self.render_image()
        self.render_error_msg()
        self.matrix.SetImage(self.canvas)
        time.sleep(self.config.rotation_rate)

    def render_error_msg(self):
        self.msg = self.data.status
        x, y = align_text(self.font.getsize(self.msg),
                          self.matrix.width,
                          self.matrix.height)
        self.draw.text((x, y), self.msg, Color.RED, self.font)

    def render_image(self):
        img = load_image(ERROR_IMAGE, tuple(self.coords['image']['size']))
        x, y = align_image(img,
                           self.matrix.width,
                           self.matrix.height,
                           Position.CENTER,
                           Position.TOP)
        self.canvas.paste(img, (x, y + 1))
