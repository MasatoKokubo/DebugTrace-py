# setup.py
# (C) 2020 Masato Kokubo
from __future__ import absolute_import
from __future__ import unicode_literals
import os

from setuptools import setup, find_packages

try:
    with open('README.md') as f:
        readme = f.read()
except IOError:
    readme = ''

def _requires_from_file(filename):
    return open(filename).read().splitlines()

# version
here = os.path.dirname(os.path.abspath(__file__))
version = next((line.split('=')[1].strip().replace("'", '')
                for line in open(os.path.join(here, 'debugtrace', 'version.py'))
                if line.startswith('__version__')),
               '0.0.0')

setup(
    name="debugtrace",
    version=version,
    url='https://github.com/MasatoKokubo/DebugTrace-py',
    author='Masato Kokubo',
    author_email='masatokokubo@gmail.com',
    maintainer='Masato Kokubo',
    maintainer_email='masatokokubo@gmail.com',
    description='Output trace logs when debugging Python programs',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[],
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ],
)