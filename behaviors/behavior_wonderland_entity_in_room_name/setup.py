#!/usr/bin/env python

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages = ['behavior_wonderland_entity_in_room_name'],
    package_dir = {'': 'src'}
)

setup(**d)