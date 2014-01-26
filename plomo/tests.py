import os
import unittest
from shutil import copyfile
from pyexif import ExifEditor

from .cameras import CAMERAS
from .plomo import manipulate_exif

PATH = os.path.dirname(__file__)
FILE = os.path.join(PATH, 'photo.jpg')


class TestExifManipulation(unittest.TestCase):
    def setUp(self):
        copyfile(os.path.join(PATH, '../photo.jpg'), FILE)

    def tearDown(self):
        os.remove(FILE)

    def test_set_camera_data(self):
        camera = CAMERAS['fisheye2']
        manipulate_exif(FILE, camera, quiet=True)
        ee = ExifEditor(FILE)
        for key in camera:
            if isinstance(camera[key], int):
                self.assertEqual(int(ee.getTag(key)), camera[key])
            else:
                self.assertEqual(ee.getTag(key), camera[key].replace('"', ''))

if __name__ == '__main__':
    unittest.main()
