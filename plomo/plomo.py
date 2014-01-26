# -*- coding: utf-8 -*-
import os
import re
import sys
from pyexif import ExifEditor

from .cameras import CAMERAS


def is_jpg(path):
    return bool(re.search('\.jpe?g$', path))


def manipulate_exif(path, camera, quiet=False):
    ee = ExifEditor(path)
    success = True
    for key in camera:
        try:
            ee.setTag(key, camera[key])
        except:
            success = False
    if quiet:
        return success
    if success:
        sys.stdout.write('.')
    else:
        sys.stdout.write('F')
    return success


def manipulate_files(path, camera):
    if os.path.isdir(path):
        for f in os.listdir(path):
            manipulate_exif(os.path.join(path, f), camera)
    elif is_jpg(path):
        manipulate_exif(path, camera)


def main():
    import argparse

    def existing_path(string):
        if os.path.exists(string):
            return string
        raise argparse.ArgumentTypeError('The path does not exist')

    def camera_type(string):
        if string in CAMERAS:
            return CAMERAS[string]
        raise argparse.ArgumentTypeError('Unknown camera')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path',
        help='Path to the photo or the folder containing the photos '
             'you want to manipulate the EXIF information',
        type=existing_path
    )
    parser.add_argument(
        'camera',
        help='Choose one of the following cameras: "%s"' %
             '", "'.join(CAMERAS.keys()),
        type=camera_type
    )
    args = parser.parse_args()

    manipulate_files(args.path, args.camera)


if __name__ == '__main__':
    main()
