#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    name="odk2odm",
    description="odk2odm provides functionalities to transfer data from an ODK server to a (Web)ODM server",
    long_description=readme + "\n\n",
    url="https://github.com/localdevices/odk2odm.git",
    author="Ivan Gayton",
    author_email="ivan.gayton@hotosm.org",
    packages=find_packages(),
    package_dir={"odk2odm": "odk2odm"},
    test_suite="tests",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    python_requires=">=3.8",
    install_requires=[
        "requests",
        "exifread",
        "Pillow",
        "qrcode",
    ],
    extras_require={
        "dev": ["pytest", "pytest-cov"],
        "optional": [],
    },
    scripts=["scripts/attachments"],
    entry_points="""
    """,
    include_package_data=True,
    license="GPLv3",
    zip_safe=False,
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Photogrammetry",
        "License :: OSI Approved :: ???",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="OpenDataKit, OpenDroneMap",
)
