import time
from typing import List

from data.forex import Forex
from renderer.ticker import TickerRenderer
from util.utils import build_forex_img


class ForexRenderer(TickerRenderer):
    """
    Renderer for Forex objects

    Attributes:
        forex (list):           List of forex
    """

    def __init__(self, matrix, canvas, draw, config, data):
        super().__init__(matrix, canvas, draw, config, data)
        self.forex: List[Forex] = data.forex

        if self.config.layout.show_logos:
            for pair in self.forex:
                pair.img = build_forex_img(pair.img_url, tuple(self.coords['forex']['image']['size']))

    def render(self):
        for pair in self.forex:
            self.clear()
            self.render_name(pair.name)
            self.render_price(str(pair.price), 'forex')
            self.render_percentage_change(pair.pct_change, pair.value_change)
            if self.coords['options']['image'] and self.config.layout.show_logos:
                self.render_image(pair.img)
            elif self.coords['options']['history_chart']:
                self.render_chart(pair.prev_close, pair.chart_prices, pair.value_change)
            self.matrix.SetImage(self.canvas)
            time.sleep(self.config.rotation_rate)
