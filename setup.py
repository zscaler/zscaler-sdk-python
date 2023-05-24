# -*- coding: utf-8 -*-
from setuptools import setup

packages = ["zscaler"]

package_data = {"": ["*"]}

install_requires = ["zscaler-sdk-python>=1.0.0"]

setup_kwargs = {
    "name": "zscaler-sdk-python",
    "version": "1.0.0",
    "description": "Framework for interacting with Zscaler Cloud via API",
    "author": "Zscaler Technology Alliances",
    "author_email": "zscaler-partner-labs@z-bd.com",
    "maintainer": None,
    "maintainer_email": None,
    "url": "https://github.com/zscaler/zscaler-sdk-python",
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "python_requires": ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
}


setup(**setup_kwargs)
