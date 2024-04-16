# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os
import re


def get_version():
    # Define the path to the __init__.py file
    init_path = os.path.join(os.path.dirname(__file__), "zscaler", "__init__.py")
    # Use a regular expression to find the version number
    version_pattern = re.compile(r"^__version__ = ['\"]([^'\"]*)['\"]")
    with open(init_path, "rt") as version_file:
        for line in version_file:
            match = version_pattern.search(line)
            if match:
                return match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="zscaler",
    version=get_version(),
    author="Zscaler, Inc.",
    author_email="devrel@zscaler.com",
    url="https://github.com/zscaler/zscaler-sdk-python",
    license="MIT",
    description="Official Python SDK for the Zscaler Products",
    long_description=open("LONG_DESCRIPTION.md").read(),
    long_description_content_type="text/markdown",
    test_suite="tests",
    packages=find_packages(exclude=("tests",)),
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "arrow",
        "certifi",
        "charset-normalizer",
        "idna",
        "python-box",
        "python-dateutil",
        "requests",
        "responses",
        "restfly",
        "six",
        "urllib3",
        "flatdict",
        "pyyaml",
        "xmltodict",
        "yarl",
        "pycryptodomex",
        "aenum",
        "pydash",
        "flake8",
    ],
)
