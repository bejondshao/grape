#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Grape',
    version='0.0.1',
    description='A stock analysis and selection system',
    long_description=readme,
    author='Bejond Shao',
    author_email='bejond@163.com',
    url='https://github.com/bejondshao/grape',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
