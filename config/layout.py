from dataclasses import dataclass, field
from rgbmatrix.graphics import Font
from utils import read_json, load_font
from constants import LAYOUT_FILE


@dataclass
class Layout:
    """Matrix Layout class"""
    width: int
    height: int
    coords: dict = field(init=False)
    primary_font: Font = field(init=False)
    secondary_font: Font = field(init=False)
    large_font: Font = field(init=False)
    time_font: Font = field(init=False)

    def __post_init__(self):
        self.coords = read_json(LAYOUT_FILE.format(self.width, self.height))
        self.primary_font = load_font('rpi-rgb-led-matrix/fonts/4x6.bdf')
        self.secondary_font = load_font('rpi-rgb-led-matrix/fonts/tom-thumb.bdf')
        self.large_font = load_font('rpi-rgb-led-matrix/fonts/6x9.bdf')
        self.time_font = load_font('assets/fonts/cherry-10-b.bdf')
