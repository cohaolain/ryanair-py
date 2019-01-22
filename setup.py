#!/usr/bin/env python
from setuptools import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='ryanair-py',
      version='0.0.5',
      description='A module which allows you to retrieve the cheapest flights, with/out return flights, within a fixed set of dates.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Ciarán Ó hAoláin',
      author_email='ciaran@cohaolain.ie',
      url='https://github.com/cohaolain/ryanairPython',
      packages=['ryanair'],
      classifiers=[
          "Programming Language :: Python :: 3",
          "Operating System :: OS Independent",
      ],
      )
