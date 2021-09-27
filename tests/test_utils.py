import pytest
import sys
import logging
import PIL
import utils
from rgbmatrix.graphics import Font

TEST_FILE = 'tests/test_file.json'
INVALID_FILE = 'invalid.txt'
ORIGINAL_DATA = {
    'key_bool': True,
    'key_string': 'value',
    'key_int': 1
}
TEST_STRING = 'Lorem ipsum'
TEST_IMAGE = 'assets/img/error.png'


@pytest.mark.skipif(not sys.platform.startswith('linux'), reason='Requires Linux')
class TestUtils:
    def test_read_json(self):
        j = utils.read_json(TEST_FILE)
        assert j == ORIGINAL_DATA

    def test_read_json_2(self, caplog):
        caplog.clear()
        with caplog.at_level(logging.ERROR):
            utils.read_json(INVALID_FILE)
        assert f"Couldn't find file at {INVALID_FILE}" in caplog.text

    @pytest.fixture
    def teardown_write_json_method(self):
        yield
        utils.write_json(TEST_FILE, ORIGINAL_DATA)  # Reset file content

    def test_write_json(self, teardown_write_json_method):
        new_data = {
            'new_bool': False,
            'new_string': 'String',
            'new_int': 2
        }
        utils.write_json(TEST_FILE, new_data)
        j = utils.read_json(TEST_FILE)
        assert j == new_data

    def test_text_offscreen(self):
        long_text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        result = utils.text_offscreen(long_text, 64, 6)
        assert result is True

    def test_text_offscreen_2(self):
        short_text = 'Lorem'
        result = utils.text_offscreen(short_text, 64, 6)
        assert result is False

    def test_align_text_center(self):
        x, y = utils.align_text_center(TEST_STRING, 64, 32, 4, 6)
        assert (x, y) == (10, 19)

    def test_align_text_center_2(self):
        x, y = utils.align_text_center(TEST_STRING, canvas_width=64, font_width=4)
        assert (x, y) == (10, 0)

    def test_align_text_center_3(self):
        x, y = utils.align_text_center(TEST_STRING, canvas_height=32, font_height=6)
        assert (x, y) == (0, 19)

    def test_align_text_right(self):
        x = utils.align_text_right(TEST_STRING, 64, 4)
        assert x == 20

    def test_center_image(self):
        x, y = utils.center_image(64, 32, 28, 28)
        assert (x, y) == (18, 2)

    def test_center_image_2(self):
        x, y = utils.center_image(canvas_width=64, image_width=28)
        assert (x, y) == (18, 0)

    def test_center_image_3(self):
        x, y = utils.center_image(canvas_height=32, image_height=28)
        assert (x, y) == (0, 2)

    def test_scroll_text(self):
        x = utils.scroll_text(64, 45, 63)
        assert x == 44

    def test_scroll_text_2(self):
        x = utils.scroll_text(64, -2, 1)
        assert x == 64

    def test_load_font(self):
        font = utils.load_font('rpi-rgb-led-matrix/fonts/5x7.bdf')
        assert isinstance(font, Font)
        assert font.baseline, 6
        assert font.height, 7

    def test_load_font_2(self, caplog):
        caplog.clear()
        with caplog.at_level(logging.WARNING):
            font = utils.load_font(INVALID_FILE)
        assert f"Couldn't find font {INVALID_FILE}. Setting font to default 4x6." in caplog.text
        assert isinstance(font, Font)
        assert font.baseline == 5
        assert font.height == 6

    def test_load_image(self):
        image = utils.load_image(TEST_IMAGE, (15, 15))
        assert isinstance(image, PIL.Image.Image)

    def test_load_image_2(self):
        image = utils.load_image(TEST_IMAGE)
        assert isinstance(image, PIL.Image.Image)

    def test_load_image_3(self, caplog):
        caplog.clear()
        with caplog.at_level(logging.ERROR):
            image = utils.load_image(INVALID_FILE)
        assert image is None
        assert f"Couldn't find image {INVALID_FILE}" in caplog.text

    def test_convert_currency(self):
        result = utils.convert_currency('USD', 'EUR', 15.0)
        assert isinstance(result, float)

    def test_convert_currency_2(self):
        result = utils.convert_currency('INVALID_CURR', 'INVALID_CURR_2', 45.4)
        assert result == 0.0

    def test_convert_currency_3(self):
        result = utils.convert_currency('EUR', 'USD', None)
        assert result == 0.0

    def test_market_closed(self):
        assert isinstance(utils.market_closed(), bool)

    def test_after_hours(self):
        assert isinstance(utils.after_hours(), bool)

    def test_weekend(self):
        assert isinstance(utils.weekend(), bool)

    def test_holiday(self):
        assert isinstance(utils.holiday(), bool)
