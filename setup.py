#!/usr/bin/env python3

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='hpie',
      description='Hierarchical Pie charts for pyplot',
      author='klieret',
      author_email='klieret@users.noreply.github.com',
      url='https://github.com/klieret/pyplot-hierarchical-pie',
      packages=['hpie'],
      install_requires=['matplotlib', 'typing'],
)





