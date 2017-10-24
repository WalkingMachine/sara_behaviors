#!/usr/bin/env python

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages = ['behavior_sandbox_for_test_purpose'],
    package_dir = {'': 'src'}
)

setup(**d)