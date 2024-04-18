# -*- coding: utf-8 -*-
from setuptools import setup
import os
import re

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), encoding='utf-8') as fp:
        return fp.read()
    
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


packages = [
    "zscaler",
    "zscaler.cache",
    "zscaler.errors",
    "zscaler.exceptions",
    "zscaler.ratelimiter",
    "zscaler.zia",
    "zscaler.zpa",
]

package_data = {"": ["*"]}

setup(
    name="zscaler-sdk-python",
    version=get_version(),
    description="Official Python SDK for the Zscaler Products",
    long_description=read('LONG_DESCRIPTION.md'),  # Read the content of the Markdown file
    long_description_content_type='text/markdown',  # Specify the content type as Markdown
    author="Zscaler Technology Alliances",
    author_email="devrel@zscaler.com",
    url="https://github.com/zscaler/zscaler-sdk-python",
    packages=packages,
    package_data=package_data,
    install_requires=[
        "arrow", "certifi", "charset-normalizer", "idna", "python-box",
        "python-dateutil", "requests", "responses", "restfly", "six",
        "urllib3", "flatdict", "pyyaml", "xmltodict", "yarl",
        "pycryptodomex", "aenum", "pydash", "flake8",
    ],
    python_requires=">=3.8,<4.0",
)