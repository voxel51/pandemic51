#!/usr/bin/env python
'''
Installs pandemic51.

Copyright 2017-2020, Voxel51, Inc.
voxel51.com
'''
from setuptools import setup, find_packages


setup(
    name="pandemic51",
    version="0.1.0",
    description="Voxel51's website for monitoring the impact of the coronavirus pandemic",
    author="Voxel51, Inc.",
    author_email="dev@voxel51.com",
    url="https://github.com/voxel51/pandemic51",
    license="BSD-4-Clause",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
)
