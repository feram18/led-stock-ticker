import logging

from PIL import Image, ImageFont

import constants
from util import utils
from util.position import Position


class TestUtils:
    def setup_method(self):
        self.font = utils.load_font('4x6.ttf', 6)

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

    def test_align_image_2(self):
        img = utils.load_image('assets/img/logo.png', (15, 15))
        x = utils.align_image(img, 64, x=Position.LEFT)[0]
        assert x == 0

    def test_align_image_3(self):
        img = utils.load_image('assets/img/logo.png', (15, 15))
        x, y = utils.align_image(img, col_height=32, y=Position.CENTER)
        assert y == 11

    def test_load_font(self):
        font = utils.load_font('4x6.ttf', 6)
        assert isinstance(font, ImageFont.FreeTypeFont)

    def test_load_font_2(self):
        font = utils.load_font('4x6.ttf', 6)
        assert font.getsize(' ')[0], 4

    def test_load_font_3(self):
        font = utils.load_font('4x6.ttf', 6)
        assert font.getsize(' ')[1], 6

    def test_load_font_4(self, caplog):
        caplog.clear()
        with caplog.at_level(logging.WARNING):
            utils.load_font('invalid.ttf', 6)
        assert f"Couldn't find font {constants.FONTS_DIR}invalid.ttf" in caplog.text

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
        assert "Couldn't find image invalid.png" in caplog.text

    def test_load_image_4(self):
        image = utils.load_image('invalid.png', (15, 15))
        assert image is None

    def test_load_image_url(self):
        url = 'https://picsum.photos/200/300'
        img = utils.load_image_url(url, (10, 10))
        assert isinstance(img, Image.Image)

    def test_load_image_url_2(self, caplog):
        url = 'https://picsum.photos'
        caplog.clear()
        with caplog.at_level(logging.ERROR):
            utils.load_image_url(url, (10, 10))
        assert f'Could not get image at {url}' in caplog.text

    def test_load_image_url_3(self, caplog):
        caplog.clear()
        with caplog.at_level(logging.ERROR):
            utils.load_image_url(None, (10, 10))
        assert 'No url provided' in caplog.text

    def test_convert_currency(self):
        result = utils.convert_currency(1, 15.0)
        assert isinstance(result, float)

    def test_convert_currency_2(self):
        result = utils.convert_currency('13.1', 45.4)
        assert result == 0.0

    def test_convert_currency_3(self):
        result = utils.convert_currency(1.23, None)
        assert result == 0.0

    def test_build_forex_img(self):
        urls = [
            constants.FLAG_URL.format('cad'),
            constants.FLAG_URL.format('eur')
        ]
        img = utils.build_forex_img(urls, (40, 20))
        assert isinstance(img, Image.Image)

    def test_build_forex_img_2(self, caplog):
        urls = [
            constants.FLAG_URL.format('invalid'),
            constants.FLAG_URL.format('invalid')
        ]
        with caplog.at_level(logging.WARNING):
            utils.build_forex_img(urls, (40, 20))
        assert 'Unable to build forex image' in caplog.text
