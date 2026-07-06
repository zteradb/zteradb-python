#!/usr/bin/env python
# -----------------------------------------------------------------------------
# File: setup.py
# Description: Packaging and distribution configuration for the ZTeraDB
#              Python Client.
#
# Licence: ZTeraDB
# Copyright (c) 2025 ZTeraDB
# -----------------------------------------------------------------------------
import os
from setuptools import setup, find_packages

base_dir = os.path.abspath(os.path.dirname(__file__))

long_description = ""
readme_path = os.path.join(base_dir, "README.md")
if os.path.exists(readme_path):
    with open(readme_path, encoding="utf-8") as f:
        long_description = f.read()

version_file_path = os.path.join(base_dir, "zteradb/version.py")

def get_version():
    if os.path.exists(version_file_path):
        with open(version_file_path, encoding="utf-8") as f:
            for line in f:
                if line.startswith('__version__'):
                    delim = '"' if '"' in line else "'"
                    return line.split(delim)[1]
            raise RuntimeError("Unable to find version string.")

package_version = "2.0.1"

setup(
    name="zteradb",
    version=get_version(),
    packages=find_packages(),
    install_requires=[],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='ZTeraDB',
    author_email='dev@zteradb.com',
    description="High-performance async Python client for ZTeraDB utilizing raw TCP socket transport layer.",
    url='https://github.com/zteradb/zteradb-python.git',
    tests_require=["unittest"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Database :: Front-Ends",
        "Framework :: AsyncIO",
    ],
    python_requires='>=3.8',
    license='ZTeraDB',
    extras_require = {
        "dev": [
            "pytest>=8.0.0",
            "pytest-asyncio>=0.23.0",
            "coverage>=7.0.0",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)

