#!/usr/bin/env python
from setuptools import setup
from os.path import join, dirname

setup(name='ryanair-py',
      version='0.0.1',
      description='A module which allows you to retrieve the cheapest flights, with/out return flights, within a fixed set of dates.',
      long_description=open(join(dirname(__file__), 'README.md')).read(),
      author='Ciarán Ó hAoláin',
      author_email='ciaran@cohaolain.ie',
      url='https://github.com/cohaolain/ryanairPython',
      packages=['ryanair'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        ],
      )
