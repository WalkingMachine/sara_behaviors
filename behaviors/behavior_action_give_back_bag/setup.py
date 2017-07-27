#!/usr/bin/env python

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages = ['behavior_action_give_back_bag'],
    package_dir = {'': 'src'}
)

setup(**d)