# -*- coding: utf-8 -*-
import os
import re
from pyexif import ExifEditor
from cameras import CAMERAS


def is_jpg(path):
    return bool(re.search('\.jpe?g$', path))


def manipulate_exif(path, camera):
    ee = ExifEditor(path)
    for key in CAMERAS[camera]:
        try:
            ee.setTag(key, CAMERAS[camera][key])
        except Exception, e:
            print(e)


def manipulate_files(path, camera):
    if os.path.isdir(path):
        for f in os.listdir(path):
            manipulate_exif(os.path.join(path, f), camera)
    elif is_jpg(path):
        manipulate_exif(path, camera)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path',
        help='Path to the photo or the folder containing the photos '
             'you want to manipulate the EXIF information'
    )
    parser.add_argument(
        'camera',
        help='Choose one of the following cameras: "%s"' %
             '", "'.join(CAMERAS.keys())
    )
    args = parser.parse_args()

    if os.path.exists(args.path):
        manipulate_files(args.path, args.camera)
    else:
        print('File or folder does not exist')


if __name__ == '__main__':
    main()
