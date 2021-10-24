from abc import ABC, abstractmethod
from data.color import Color


class Renderer(ABC):
    """
    Base Renderer abstract class

    Arguments:
        matrix (rgbmatrix.RGBMatrix):                   RGBMatrix instance
        canvas (rgbmatrix.Canvas):                      Canvas associated with matrix
        config (config.MatrixConfig):                   MatrixConfig instance

    Attributes:
        primary_font (rgbmatrix.graphics.Font):         Primary font
        secondary_font (rgbmatrix.graphics.Font):       Secondary font
        large_font (rgbmatrix.graphics.Font):           Large font
        text_color (rgbmatrix.graphics.Color):          Default text color
    """

    def __init__(self, matrix, canvas, config):
        self.matrix = matrix
        self.canvas = canvas
        self.config = config
        self.secondary_font = self.config.layout.secondary_font  # 4x6
        self.primary_font = self.config.layout.primary_font  # TomThumb
        self.large_font = self.config.layout.large_font  # 6x9
        self.text_color = Color.WHITE

    @abstractmethod
    def render(self):
        pass
