# -*- coding: utf-8 -*-
import os
import re

from setuptools import find_packages, setup

long_description = (
    "Zscaler SDK Python\n"
    "==================\n\n"
    "The Zscaler SDK Python provides a uniform and easy-to-use interface for each of the Zscaler product APIs.\n\n"
    "Getting Started\n"
    "---------------\n"
    "Install using pip:\n\n"
    ".. code-block:: shell\n\n"
    "    $ pip install zscaler\n\n"
    "What you need\n"
    "-------------\n\n"
    "Before you can interact with any of the Zscaler APIs, you need to generate API keys or retrieve tenancy information for each product that you are interfacing with. Once you have the requirements and you have installed Zscaler SDK Python, you're ready to go.\n\n"
    "- `ZPA API Credentials <https://help.zscaler.com/zpa/getting-started-zpa-api>`_\n"
    "- `ZIA API Credentials <https://help.zscaler.com/zia/getting-started-zia-api>`_\n\n"
    "Look for our quickstart guide here!\n\n"
    "- `Zscaler SDK Python Quickstart <https://github.com/zscaler/zscaler-sdk-python>`_\n"
)

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
    name="zscaler-sdk-python",
    version=get_version(),
    author="Zscaler, Inc.",
    author_email="devrel@zscaler.com",
    url="https://github.com/zscaler/zscaler-sdk-python",
    license="MIT",
    description="Official Python SDK for the Zscaler Products",
    long_description=long_description,
    long_description_content_type='text/x-rst',
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
