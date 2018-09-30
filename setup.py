import os
import re
from codecs import open

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pytelemetry',
    version=find_version('pytelemetry', '__init__.py'),
    description='F1 2018 Telemetry',
    long_description=long_description,
    author='Alessandro Bessi',
    author_email='alessandro.bessi@mail.com',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Data scientists',
        'Topic :: Scientific/Engineering :: Racing Simulation',

        # Pick your license as you wish
        'License :: Proprietary license',

        # Specify the Python versions you support here.
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    keywords='F1 2018 telemetry',  # TODO: update
    packages=find_packages(exclude=['build', 'data', 'dist', 'docs', 'tests']),
    python_requires='>=3.6',
    install_requires=[
        'netifaces==0.10.7',
        'matplotlib==2.1.2'
    ]
)
