#! /usr/bin/python

import argparse
import colorsys
import os
import re

import sys

DEFAULT_PREFIX = 'image_'


def generate_bg_values(number):
    """Generate Background /Hexadecimal Color Values.

    Returns a list of RGB hexadecimal color codes by distributing the Hue range
    uniformly.
    """
    colors = []
    for i in range(number):
        colors.append(colorsys.hsv_to_rgb(float(i)/float(number), 1, 1))

    return ['%0.2x%0.2x%0.2x' % (x[0]*255, x[1]*255, x[2]*255) for x in colors]


def print_header(args, bg_values):
    print 80 * '='
    print 'Format: {}'.format(args.format)
    print 'Size: {}'.format(args.size)
    print 'Image Background Colors: '
    for num in range(args.number):
        print ' - {}: {}'.format(num+1, bg_values[num])
    print 80 * '='


def generate_and_save_images(args):
    bg_values = generate_bg_values(args.number)
    print_header(args, bg_values)
    if args.dry_run:
        print 'Dry Run...'
        return

    padding = (args.number / 10) + 1
    for num in range(args.number):
        padded_num = str(num+1).zfill(padding)
        filename = '{}{}.{}'.format(args.prefix, padded_num, args.format)
        filepath = os.path.join(args.destination, filename)
        with open(filepath, 'wb') as file:
            file.write('placeholder')


def check_size(value):
    """Custom argument type to """
    match = re.match(r'(\d+x\d+)|(\d+)', value)
    if match:
        if match.group(2):
            return '{}x{}'.format(match.group(2), match.group(2))
        else:
            return match.group(1)
    else:
        raise argparse.ArgumentTypeError(
            'Size must be a single number or match "<width>x<heigth>"'
        )


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number', default=12, type=int,
                        help='Number of images to generate. Default: 12')
    parser.add_argument('-s', '--size', default='1024x768', type=check_size,
                        help=('Size of image in the format "<width>x<height>. '
                              'Can also be a single number, in which case the '
                              ' generated images will be a square. Default: '
                              '1024x768.'))
    parser.add_argument('-f', '--format', default='jpg',
                        choices=('jpg', 'gif', 'png', 'bmp'),
                        help='Image file format. Default: jpg')
    parser.add_argument('-d', '--dry-run', default=False, action='store_true',
                        help=('Only print debug info about the images about '
                              'to be generated.'))
    parser.add_argument('-p', '--prefix', default=DEFAULT_PREFIX,
                        help='Images filename prefix. Default: "image_".')
    parser.add_argument('destination',
                        help='Directory in which to save image files.')

    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])
    generate_and_save_images(args)


if __name__ == '__main__':
    main()
