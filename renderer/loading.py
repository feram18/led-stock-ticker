from rgbmatrix.graphics import DrawText
from renderer.renderer import Renderer
from version import __version__
from constants import LOADING_IMAGE
from util.utils import align_text, load_image, align_image
from util.position import Position
from util.color import Color


class Loading(Renderer):
    """Render a splash screen while tickers' data is being fetched"""

    def render(self):
        self.canvas.Clear()

        self.render_logo()
        self.render_version()

        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def render_version(self):
        x, y = align_text(__version__,
                          Position.CENTER,
                          Position.BOTTOM,
                          self.canvas.width,
                          self.canvas.height,
                          self.secondary_font.baseline - 1,
                          self.secondary_font.height)

        DrawText(self.canvas, self.secondary_font, x, y, Color.ORANGE, __version__)

    def render_logo(self):
        img = load_image(LOADING_IMAGE, (28, 28))
        x_offset, y_offset = align_image(img,
                                         Position.CENTER,
                                         Position.CENTER,
                                         self.canvas.width,
                                         self.canvas.height)
        self.canvas.SetImage(img, x_offset, y_offset - 2)
