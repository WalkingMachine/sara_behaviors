#!/usr/bin/env python

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages = ['behavior_sara_action_executor'],
    package_dir = {'': 'src'}
)

setup(**d)