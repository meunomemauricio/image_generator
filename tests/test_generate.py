import argparse
import unittest

from generate import check_size, generate_bg_values


class CheckSizeTests(unittest.TestCase):

    def test_invalid_size(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            check_size('invalid')

    def test_single_number_size(self):
        size = check_size('100')

        self.assertEquals(size, '100x100')

    def test_full_size(self):
        size = check_size('100x200')

        self.assertEquals(size, '100x200')


class GenerateBGValuesTests(unittest.TestCase):

    def test_generated_bg_Values(self):
        number = 3

        values = generate_bg_values(3)

        self.assertEqual(len(values), number)
        self.assertEqual(values, ['ff0000', '00ff00', '0000ff'])
