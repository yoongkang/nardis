#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import io
import os

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


setup(
    name="nardis",
    version="0.0.6",
    description="A web framework based on ASGI",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Yoong Kang Lim",
    author_email="yoongkang.lim@gmail.com",
    python_requires=">=3.6",
    url="https://github.com/yoongkang/nardis",
    packages=find_packages("."),
    install_requires=[
        "typing_extensions",
        "uvicorn",
    ],
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)