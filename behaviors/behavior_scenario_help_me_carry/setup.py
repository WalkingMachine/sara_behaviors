#!/usr/bin/env python

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages = ['behavior_scenario_help_me_carry'],
    package_dir = {'': 'src'}
)

setup(**d)