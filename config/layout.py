from dataclasses import dataclass, field

from PIL import ImageFont

from constants import LAYOUT_FILE
from util.utils import read_json, load_font


@dataclass
class Layout:
    """Matrix Layout class"""
    width: int
    height: int
    coords: dict = field(init=False)
    primary_font: ImageFont = field(init=False)
    secondary_font: ImageFont = field(init=False)
    large_font: ImageFont = field(init=False)
    clock_font: ImageFont = field(init=False)
    show_logos: bool = field(init=False)

    def __post_init__(self):
        self.coords = read_json(LAYOUT_FILE.format(self.width, self.height))
        self.primary_font = load_font(self.coords['fonts']['primary'])
        self.clock_font = load_font(self.coords['fonts']['clock'])
        self.show_logos = False
