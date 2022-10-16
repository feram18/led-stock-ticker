import time
from abc import ABC, abstractmethod
from typing import Tuple

import multitasking
from PIL import Image, ImageDraw, ImageFont
from rgbmatrix import RGBMatrix

from config.matrix_config import MatrixConfig
from constants import TEXT_SCROLL_SPEED
from util.color import Color
from util.direction import Direction


class Renderer(ABC):
    """
    Base Renderer abstract class

    Arguments:
        matrix (rgbmatrix.RGBMatrix):           RGBMatrix instance
        canvas (PIL.Image):                     Canvas associated with matrix
        config (config.MatrixConfig):              MatrixConfig instance

    Attributes:
        primary_font (PIL.ImageFont):           Primary font
        text_color (util.Color):                Default text color
    """

    def __init__(self, matrix, canvas, draw, config):
        self.matrix: RGBMatrix = matrix
        self.canvas: Image = canvas
        self.draw: ImageDraw = draw
        self.config: MatrixConfig = config
        self.primary_font: ImageFont = self.config.layout.primary_font
        self.text_color: ImageFont = Color.WHITE

    @abstractmethod
    def render(self):
        pass

    def clear(self):
        self.draw.rectangle(((0, 0), (self.matrix.width, self.matrix.height)), fill=Color.BLACK)

    @multitasking.task
    def scroll_text(self, text: str, font: ImageFont, text_color: tuple, bg_color: tuple, start_pos: Tuple[int, int]):
        """
        Scroll string of text on canvas
        :param text: (str) text to scroll
        :param font: (ImageFont) text font
        :param text_color: (tuple) text font color
        :param bg_color: (tuple) text background color
        :param start_pos: (int) text starting x-position
        """
        x, begin = start_pos[0], start_pos[0]
        end = (self.matrix.width, start_pos[1] + font.getsize(text)[1] - 1)
        direction = Direction.LEFT
        new_direction = True
        time_started = time.time()
        finished = False

        while not finished:
            self.draw.rectangle(((x, start_pos[1]), end), bg_color)
            self.draw.text((x, start_pos[1]), text, text_color, font)
            self.matrix.SetImage(self.canvas)

            length = font.getsize(text)[0] + x

            if length < self.matrix.width:  # End of text is now visible
                direction = Direction.RIGHT
                new_direction = True
            elif x == begin:  # Text is back to starting position
                direction = Direction.LEFT
                new_direction = True

            if direction is Direction.LEFT:
                x -= 1
            else:
                x += 1

            if new_direction:
                time.sleep(1.5)
                new_direction = False
            else:
                time.sleep(TEXT_SCROLL_SPEED)

            if time.time() - time_started >= self.config.rotation_rate:
                finished = True
