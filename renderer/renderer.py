from abc import ABC, abstractmethod


class Renderer(ABC):
    """
    Base Renderer abstract class

    Arguments:
        matrix (rgbmatrix.RGBMatrix):       RGBMatrix instance
        canvas (rgbmatrix.Canvas):          Canvas associated with matrix
    """

    def __init__(self, matrix, canvas):
        self.matrix = matrix
        self.canvas = canvas

    @abstractmethod
    def render(self):
        pass
