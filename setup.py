#!/usr/bin/env python
# Install script for some random utils.
# Max Melin

import os
from setuptools import setup, find_packages


setup(
    name = 'neurodatatypes',
    version = '0.1.0',
    author = 'Max Melin',
    author_email = 'mmelin@g.ucla.edu',
    description = 'General purpose classes for manipulating neural datasets.',
    packages = find_packages()
)
