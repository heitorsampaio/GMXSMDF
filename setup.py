#!/usr/bin/env python3
from distutils.core import setup

VERSION = '0.0.1'
setup(
    name = 'gmxsmdscript',
    version = VERSION,
    description = 'Gromacs simple MD framework',
    author = 'Heitor Sampaio',
    author_email = 'horlando.heitor@gmail.com',
    url = 'https://github.com/heitorsampaio/GMXSMDF',
    download_url = 'https://github.com//heitorsampaio/GMXSMDF/tarball/%s' % VERSION,
    py_modules = ['gmxsmdscript'],
 )
