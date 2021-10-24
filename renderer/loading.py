from rgbmatrix.graphics import DrawText
from renderer.renderer import Renderer
from version import __version__
from constants import LOADING_IMAGE
from utils import align_text_center, load_image, center_image
from data.color import Color


class Loading(Renderer):
    """Render a splash screen while tickers' data is being fetched"""

    def render(self):
        self.canvas.Clear()

        self.render_logo()
        self.render_version()

        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def render_version(self):
        x = align_text_center(string=__version__,
                              canvas_width=self.canvas.width,
                              font_width=self.secondary_font.baseline - 1)[0]
        y = self.canvas.height

        DrawText(self.canvas, self.secondary_font, x, y, Color.ORANGE, __version__)

    def render_logo(self):
        img = load_image(LOADING_IMAGE, (28, 28))
        x_offset, y_offset = center_image(self.canvas.width,
                                          self.canvas.height,
                                          img.width,
                                          img.height)
        self.canvas.SetImage(img, x_offset, y_offset - 2)
