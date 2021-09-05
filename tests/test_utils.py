import unittest
import sys
import PIL
from unittest import TestCase
from rgbmatrix.graphics import Font
from utils import *

TEST_FILE = 'tests/test_file.json'
INVALID_FILE = 'invalid.txt'
ORIGINAL_DATA = {
    'key_bool': True,
    'key_string': 'value',
    'key_int': 1
}
TEST_STRING = 'Lorem ipsum'
TEST_IMAGE = 'assets/img/error.png'


class TestUtils(TestCase):
    def test_read_json(self):
        j = read_json(TEST_FILE)
        self.assertDictEqual(j, ORIGINAL_DATA)

    def test_read_json_2(self):
        with self.assertRaises(FileNotFoundError) as cm, self.assertLogs(level=logging.ERROR) as cm_:
            read_json(INVALID_FILE)
        self.assertEqual(cm.exception.errno, 2)
        self.assertIn(f'ERROR:root:Could not find file at {INVALID_FILE}', cm_.output)

    def test_write_json(self):
        new_data = {
            'new_bool': False,
            'new_string': 'String',
            'new_int': 2
        }
        write_json(TEST_FILE, new_data)
        j = read_json(TEST_FILE)
        self.assertDictEqual(j, new_data)
        write_json(TEST_FILE, ORIGINAL_DATA)  # Reset file content

    def test_text_offscreen(self):
        long_text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        result = text_offscreen(long_text, 64, 6)
        self.assertTrue(result)

    def test_text_offscreen_2(self):
        short_text = 'Lorem'
        result = text_offscreen(short_text, 64, 6)
        self.assertFalse(result)

    def test_align_text_center(self):
        x, y = align_text_center(TEST_STRING, 64, 32, 4, 6)
        self.assertEqual((x, y), (10, 19))

    def test_align_text_center_2(self):
        x, y = align_text_center(TEST_STRING, canvas_width=64, font_width=4)
        self.assertEqual((x, y), (10, 0))

    def test_align_text_center_3(self):
        x, y = align_text_center(TEST_STRING, canvas_height=32, font_height=6)
        self.assertEqual((x, y), (0, 19))

    def test_align_text_center_4(self):
        x, y = align_text_center(TEST_STRING, 32, 64, 'w', 'h')
        self.assertEqual((x, y), (0, 0))

    def test_align_text_right(self):
        x = align_text_right(TEST_STRING, 64, 4)
        self.assertEqual(x, 20)

    def test_align_text_right_2(self):
        x = align_text_right(TEST_STRING, 64, 'w')
        self.assertEqual(x, 0)

    def test_center_image(self):
        x, y = center_image(64, 32, 28, 28)
        self.assertEqual((x, y), (18, 2))

    def test_center_image_2(self):
        x, y = center_image(canvas_width=64, image_width=28)
        self.assertEqual((x, y), (18, 0))

    def test_center_image_3(self):
        x, y = center_image(canvas_height=32, image_height=28)
        self.assertEqual((x, y), (0, 2))

    def test_center_image_4(self):
        x, y = center_image(64, 32, 'w', 'h')
        self.assertEqual((x, y), (0, 0))

    def test_scroll_text(self):
        x = scroll_text(64, 45, 63)
        self.assertEqual(x, 44)

    def test_scroll_text_2(self):
        x = scroll_text(64, -2, 1)
        self.assertEqual(x, 64)

    @unittest.skipUnless(sys.platform.startswith('linux'), 'Requires Linux')
    def test_load_font(self):
        font = load_font('rpi-rgb-led-matrix/fonts/5x7.bdf')
        self.assertIsInstance(font, Font)
        self.assertEqual(font.baseline, 6)
        self.assertEqual(font.height, 7)

    @unittest.skipUnless(sys.platform.startswith('linux'), 'Requires Linux')
    def test_load_font_2(self):
        with self.assertLogs(level=logging.WARNING) as cm:
            font = load_font(INVALID_FILE)
        self.assertIn(f"WARNING:root:Couldn't load font {INVALID_FILE}. Setting font to default 4x6.", cm.output)
        self.assertIsInstance(font, Font)
        self.assertEqual(font.baseline, 5)
        self.assertEqual(font.height, 6)

    def test_load_image(self):
        image = load_image(TEST_IMAGE, (15, 15))
        self.assertIsInstance(image, PIL.Image.Image)

    def test_load_image_2(self):
        image = load_image(TEST_IMAGE)
        self.assertIsInstance(image, PIL.Image.Image)

    def test_load_image_3(self):
        image = load_image(TEST_IMAGE, ('a', 'b'))
        self.assertIsInstance(image, PIL.Image.Image)

    def test_load_image_4(self):
        with self.assertLogs(level=logging.ERROR) as cm:
            image = load_image(INVALID_FILE)
        self.assertIsNone(image)
        self.assertIn(f"ERROR:root:Couldn't find image {INVALID_FILE}", cm.output)

    def test_convert_currency(self):
        result = convert_currency('USD', 'EUR', 15.0)
        self.assertIsInstance(result, float)

    def test_convert_currency_2(self):
        result = convert_currency('INVALID_CURR', 'INVALID_CURR_2', 45.4)
        self.assertEqual(result, 0.0)

    def test_convert_currency_3(self):
        result = convert_currency('EUR', 'USD', 'invalid_type')
        self.assertEqual(result, 0.0)

    def test_market_closed(self):
        self.assertIsInstance(market_closed(), bool)

    def test_after_hours(self):
        self.assertIsInstance(after_hours(), bool)

    def test_weekend(self):
        self.assertIsInstance(weekend(), bool)

    def test_holiday(self):
        self.assertIsInstance(holiday(), bool)
