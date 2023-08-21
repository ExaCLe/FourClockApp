from unittest import TestCase

from main import rgb_to_hex, str_to_tuple


class Test(TestCase):
    def test_rgb_to_hex(self):
        self.assertEqual(rgb_to_hex((255, 0, 0)), "#ff0000")
        self.assertEqual(rgb_to_hex((0, 255, 0)), "#00ff00")
        self.assertEqual(rgb_to_hex((0, 0, 255)), "#0000ff")
        self.assertEqual(rgb_to_hex((128, 128, 128)), "#808080")
        self.assertEqual(rgb_to_hex((0, 0, 0)), "#000000")
        self.assertEqual(rgb_to_hex((255, 255, 255)), "#ffffff")
        self.assertEqual(rgb_to_hex((16, 32, 64)), "#102040")
        self.assertEqual(rgb_to_hex((255, 125, 0)), "#ff7d00")


class TestStrToTuple(TestCase):
    def test_with_brackets(self):
        self.assertEqual(str_to_tuple('(255, 0, 0)'), (255, 0, 0))

    def test_without_brackets(self):
        self.assertEqual(str_to_tuple('255, 0, 0'), (255, 0, 0))

    def test_custom_1(self):
        self.assertEqual(str_to_tuple(' (128, 255, 64)'), (128, 255, 64))

    def test_custom_2(self):
        self.assertEqual(str_to_tuple('0, 128, 255'), (0, 128, 255))

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            str_to_tuple('255, 0, a')
