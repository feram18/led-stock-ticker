import sys
import logging

import pytest
from PIL import Image
from PIL import ImageFont

import constants
from util import utils
from util.position import Position


@pytest.mark.skipif(not sys.platform.startswith('linux'), reason='Requires Linux')
class TestUtils:
    def setup_method(self):
        self.font = utils.load_font('tom-thumb.pil')

    def test_read_json(self, tmpdir):
        tmp_file = tmpdir.join('temp.json')
        content = {
            "key_bool": True,
            "key_string": "String",
            "key_int": 1
        }
        utils.write_json(tmp_file, content)
        dict_ = utils.read_json(tmp_file)
        assert dict_ == content

    def test_read_json_2(self, caplog):
        caplog.clear()
        with caplog.at_level(logging.ERROR):
            utils.read_json('invalid.json')
        assert "Couldn't find file at invalid.json" in caplog.text

    def test_write_json(self, tmpdir):
        tmp_file = tmpdir.join('temp.json')
        new_data = {
            "key_bool": False,
            "key_string": None,
            "key_int": 0
        }
        utils.write_json(tmp_file, new_data)
        dict_ = utils.read_json(tmp_file)
        assert dict_ == new_data

    def test_off_screen(self):
        long_text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        result = utils.off_screen(64, self.font.getsize(long_text)[0])
        assert result is True

    def test_off_screen_2(self):
        short_text = 'Lorem'
        result = utils.off_screen(64, self.font.getsize(short_text)[0])
        assert result is False

    def test_align_text(self):
        x, y = utils.align_text(self.font.getsize('Lorem ipsum'), 64, 32, Position.CENTER, Position.CENTER)
        assert (x, y) == (11, 13)

    def test_align_text_2(self):
        x = utils.align_text(self.font.getsize('Lorem ipsum'), col_width=64, x=Position.CENTER)[0]
        assert x == 11

    def test_align_text_3(self):
        y = utils.align_text(self.font.getsize('Lorem ipsum'), col_height=32, y=Position.CENTER)[1]
        assert y == 13

    def test_align_text_4(self):
        x = utils.align_text(self.font.getsize('Lorem ipsum'), col_width=64, x=Position.RIGHT)[0]
        assert x == 22

    def test_align_text_5(self):
        y = utils.align_text(self.font.getsize('Lorem ipsum'), col_height=32, y=Position.BOTTOM)[1]
        assert y == 26

    def test_align_image(self):
        img = utils.load_image('assets/img/logo.png', (15, 15))
        x, y = utils.align_image(img, 64, 32)
        assert (x, y) == (25, 11)

    def test_load_font(self):
        font = utils.load_font('tom-thumb.pil')
        assert isinstance(font, ImageFont.ImageFont)

    def test_load_font_2(self):
        font = utils.load_font('tom-thumb.pil')
        assert font.getsize(' ')[0], 4

    def test_load_font_3(self):
        font = utils.load_font('tom-thumb.pil')
        assert font.getsize(' ')[1], 6

    def test_load_font_4(self, caplog):
        caplog.clear()
        with caplog.at_level(logging.WARNING):
            utils.load_font('invalid.pil')
        assert f"Couldn't find font {constants.FONTS_DIR}invalid.pil" in caplog.text

    def test_load_image(self):
        image = utils.load_image('assets/img/error.png', (15, 15))
        assert isinstance(image, Image.Image)

    def test_load_image_2(self):
        image = utils.load_image('assets/img/error.png', (15, 15))
        assert image.size <= (15, 15)

    def test_load_image_3(self, caplog):
        caplog.clear()
        with caplog.at_level(logging.ERROR):
            utils.load_image('invalid.png', (15, 15))
        assert f"Couldn't find image invalid.png" in caplog.text

    def test_load_image_4(self):
        image = utils.load_image('invalid.png', (15, 15))
        assert image is None

    def test_convert_currency(self):
        result = utils.convert_currency('USD', 'EUR', 15.0)
        assert isinstance(result, float)

    def test_convert_currency_2(self):
        result = utils.convert_currency('INVALID_CURR', 'INVALID_CURR_2', 45.4)
        assert result == 0.0

    def test_convert_currency_3(self):
        result = utils.convert_currency('EUR', 'USD', None)
        assert result == 0.0

    def test_after_hours(self):
        assert isinstance(utils.after_hours(), bool)

    def test_weekend(self):
        assert isinstance(utils.weekend(), bool)

    def test_holiday(self):
        assert isinstance(utils.holiday(), bool)
