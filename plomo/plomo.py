# -*- coding: utf-8 -*-
import os
import re
import sys
from pyexif import ExifEditor

from .equipment import CAMERAS


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
    success = True
    if os.path.isdir(path):
        for f in os.listdir(path):
            if not manipulate_exif(os.path.join(path, f), camera):
                success = False
    elif is_jpg(path):
        if not manipulate_exif(path, camera):
            success = False
    return success


def open_gui(path=None, camera=None):
    from .gui import PlomoApp
    app = PlomoApp(path=path, camera=camera)
    app.master.title('Plomo')
    app.mainloop()


def main():
    import argparse

    def existing_path(string):
        if os.path.exists(string):
            return string
        raise argparse.ArgumentTypeError('The path does not exist')

    def camera_type(string):
        if string in CAMERAS:
            return string
        raise argparse.ArgumentTypeError('Unknown camera')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-g', '--gui',
        help='View the graphical interface',
        action='store_true'
    )
    parser.add_argument(
        '--path',
        help='Path to the photo or the folder containing the photos '
             'you want to manipulate the Exif information',
        type=existing_path
    )
    parser.add_argument(
        '--camera',
        help='Choose one of the following cameras: "%s"' %
             '", "'.join(CAMERAS.keys()),
        type=camera_type
    )
    args = parser.parse_args()

    if args.gui:
        open_gui(args.path, args.camera)
    elif args.path and args.camera:
        manipulate_files(args.path, CAMERAS[args.camera])
    else:
        open_gui()


if __name__ == '__main__':
    main()
