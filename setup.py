#!/usr/bin/env python3.6

from setuptools import setup, find_packages

setup(
    name='aio',
    version='0.0.0',
    description='A minimal asynchronous I/O engine',
    author='Justin R. Cutler',
    author_email='justin.r.cutler@gmail.com',
    packages=find_packages(),
    python_requires='3.6',
)
