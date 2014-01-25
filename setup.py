from setuptools import setup, find_packages


setup(
    name="plomo",
    version='0.1.0',
    description='',
    url='http://github.com/relekang/plomo',
    author='Rolf Erik Lekang',
    packages=find_packages(),
    install_requires=[
        'pyexif',
    ],
    entry_points={
        'console_scripts': [
            'plomo = plomo.plomo:main',
        ]
    }
)
