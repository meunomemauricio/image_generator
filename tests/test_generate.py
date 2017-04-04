import argparse
import os
import tempfile
import unittest

from generate import check_size, generate_bg_values, generate_and_save_images, \
    parse_args


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


class GenerateAndSaveImages(unittest.TestCase):

    def setUp(self):
        self.destination = tempfile.mkdtemp()

    def test_dry_run(self):
        """Should not generate any file."""
        args = parse_args(['-d', self.destination])

        generate_and_save_images(args)

        self.assertFalse(os.listdir(self.destination))

    def test_generate_png_image(self):
        """Filename should have PNG extention."""
        args = parse_args(['-f', 'png', '-n', '1', self.destination])
        expected_filename = 'image_1.png'

        generate_and_save_images(args)

        files = os.listdir(self.destination)
        self.assertEqual(len(files), 1)
        self.assertIn(expected_filename, files)

    def test_generate_gif_image(self):
        """Filename should have GIF extention."""
        args = parse_args(['-f', 'gif', '-n', '1', self.destination])
        expected_filename = 'image_1.gif'

        generate_and_save_images(args)

        files = os.listdir(self.destination)
        self.assertEqual(len(files), 1)
        self.assertIn(expected_filename, files)

    def test_generate_bmp_image(self):
        """Filename should have BMP extention."""
        args = parse_args(['-f', 'bmp', '-n', '1', self.destination])
        expected_filename = 'image_1.bmp'

        generate_and_save_images(args)

        files = os.listdir(self.destination)
        self.assertEqual(len(files), 1)
        self.assertIn(expected_filename, files)

    def test_generate_one_image(self):
        """Should successfully generate a file."""
        args = parse_args(['-n', '1', self.destination])
        expected_filename = 'image_1.jpg'

        generate_and_save_images(args)

        files = os.listdir(self.destination)
        self.assertEqual(len(files), 1)
        self.assertIn(expected_filename, files)

    def test_generate_three_images(self):
        """Should successfully generate three files."""
        args = parse_args(['-n', '3', self.destination])
        filenames  = ['image_{}.jpg'.format(x) for x in range(1, 3+1)]

        generate_and_save_images(args)

        files = os.listdir(self.destination)
        self.assertEqual(len(files), 3)
        for filename in filenames:
            self.assertIn(filename, files)

    def test_generate_ten_images(self):
        """Numbers in filenames should be propperly padded."""
        args = parse_args(['-n', '10', self.destination])
        filenames  = ['image_{:02d}.jpg'.format(x) for x in range(1, 10+1)]

        generate_and_save_images(args)

        files = os.listdir(self.destination)
        self.assertEqual(len(files), 10)
        for filename in filenames:
            self.assertIn(filename, files)

    def test_different_filename_prefix(self):
        """The user should be able to specify a different filename prefix."""
        args = parse_args(['-p', 'prefix_', '-n', '1', self.destination])

        generate_and_save_images(args)

        self.assertIn('prefix_1.jpg', os.listdir(self.destination))
