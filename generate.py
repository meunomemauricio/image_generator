#! /usr/bin/python

import argparse
import colorsys
import re

API_URL = 'https://dummyimage.com/{size}/{bg}/{fg}.{fmt}?text={txt}'


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
    for n in range(args.number):
        print ' - {}: {}'.format(n+1, bg_values[n])
    print 80 * '='


def generate_and_save_images(args):
    fg = 'FFFFFF'
    bg_values = generate_bg_values(args.number)

    print_header(args, bg_values)

    if args.dry_run:
        print 'Dry Run...'
        return


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


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number', default=12, type=int,
                        help='Number of images to generate. Default: 12')
    parser.add_argument('-s', '--size', default='1024x768', type=check_size,
                        help=('Size of image in the format "<width>x<height>. '
                              'Can also be a single number, in which case the '
                              ' generated images will be a square. Default: '
                              '1024x768.'))
    parser.add_argument('-f', '--format', default='jpeg',
                        choices=('jpeg', 'gif', 'png'),
                        help='Image file format. Default: jpeg')
    parser.add_argument('-d', '--dry-run', default=False, action='store_true',
                        help=('Only print debug info about the images about '
                              'to be generated.'))

    return parser.parse_args()


def main():
    args = parse_args()
    generate_and_save_images(args)

if __name__ == '__main__':
    main()
