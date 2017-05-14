import argparse
import os
import tempfile
import unittest

from mock import mock

from generate import (check_size, generate_and_save_images, generate_bg_values,
                      parse_args)


class CheckSizeTests(unittest.TestCase):

    def test_invalid_size(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            check_size('invalid')

    def test_single_number_size(self):
        size = check_size('100')

        self.assertEquals(size, (100, 100))

    def test_full_size(self):
        size = check_size('100x200')

        self.assertEquals(size, (100, 200))


class GenerateBGValuesTests(unittest.TestCase):

    def test_generated_bg_values(self):
        """Should return RGB color codes in tuples."""
        expected_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

        values = generate_bg_values(3)

        self.assertEqual(values, expected_colors)
        for r, g, b in values:
            self.assertIsInstance(r, int)
            self.assertIsInstance(g, int)
            self.assertIsInstance(b, int)


class GenerateAndSaveImages(unittest.TestCase):

    def setUp(self):
        self.destination = tempfile.mkdtemp()

    @mock.patch('generate.generate_text_image', return_value='content')
    def test_dry_run(self, gen_mk):
        """Should not generate any file."""
        args = parse_args(['-d', self.destination])

        generate_and_save_images(args)

        self.assertFalse(os.listdir(self.destination))

    @mock.patch('generate.generate_text_image', return_value='content')
    def test_generate_png_image(self, gen_mk):
        """Filename should have PNG extention."""
        args = parse_args(['-f', 'png', '-n', '1', self.destination])
        expected_filename = 'image_1.png'

        generate_and_save_images(args)

        files = os.listdir(self.destination)
        self.assertEqual(len(files), 1)
        self.assertIn(expected_filename, files)

    @mock.patch('generate.generate_text_image', return_value='content')
    def test_generate_gif_image(self, gen_mk):
        """Filename should have GIF extention."""
        args = parse_args(['-f', 'gif', '-n', '1', self.destination])
        expected_filename = 'image_1.gif'

        generate_and_save_images(args)

        files = os.listdir(self.destination)
        self.assertEqual(len(files), 1)
        self.assertIn(expected_filename, files)

    @mock.patch('generate.generate_text_image', return_value='content')
    def test_generate_bmp_image(self, gen_mk):
        """Filename should have BMP extention."""
        args = parse_args(['-f', 'bmp', '-n', '1', self.destination])
        expected_filename = 'image_1.bmp'

        generate_and_save_images(args)

        files = os.listdir(self.destination)
        self.assertEqual(len(files), 1)
        self.assertIn(expected_filename, files)

    @mock.patch('generate.generate_text_image', return_value='content')
    def test_generate_one_image(self, gen_mk):
        """Should successfully generate a file."""
        args = parse_args(['-n', '1', self.destination])
        expected_filename = 'image_1.jpg'

        generate_and_save_images(args)

        files = os.listdir(self.destination)
        self.assertEqual(len(files), 1)
        self.assertIn(expected_filename, files)

    @mock.patch('generate.generate_text_image', return_value='content')
    def test_generate_three_images(self, gen_mk):
        """Should successfully generate three files."""
        args = parse_args(['-n', '3', self.destination])
        filenames  = ['image_{}.jpg'.format(x) for x in range(1, 3+1)]

        generate_and_save_images(args)

        files = os.listdir(self.destination)
        self.assertEqual(len(files), 3)
        for filename in filenames:
            self.assertIn(filename, files)

    @mock.patch('generate.generate_text_image', return_value='content')
    def test_generate_ten_images(self, gen_mk):
        """Numbers in filenames should be propperly padded."""
        args = parse_args(['-n', '10', self.destination])
        filenames  = ['image_{:02d}.jpg'.format(x) for x in range(1, 10+1)]

        generate_and_save_images(args)

        files = os.listdir(self.destination)
        self.assertEqual(len(files), 10)
        for filename in filenames:
            self.assertIn(filename, files)

    @mock.patch('generate.generate_text_image', return_value='content')
    def test_different_filename_prefix(self, gen_mk):
        """The user should be able to specify a different filename prefix."""
        args = parse_args(['-p', 'prefix_', '-n', '1', self.destination])

        generate_and_save_images(args)

        self.assertIn('prefix_1.jpg', os.listdir(self.destination))
