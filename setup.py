import os

from setuptools import find_packages, setup


def get_version():
    # Get version number from VERSION file
    with open(os.path.join(os.path.dirname(__file__), "zscaler", "__init__.py")) as version_file:
        # File has format: __version__ = '{version_number}'
        line = version_file.read().split("=")
        version_number = line[1].strip().replace("'", "")
        return version_number


setup(
    name="zscaler",
    version=get_version(),
    author="Zscaler, Inc.",
    author_email="zscaler-partner-labs@z-bd.com",
    url="https://github.com/zscaler/zscaler-sdk-python",
    license="MIT",
    description="Framework for interacting with Zscaler Cloud via API",
    long_description=open("LONG_DESCRIPTION.md").read(),
    test_suite="tests",
    packages=find_packages(exclude=("tests",)),
    python_requires=">=3.8,<4.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "python-box",
        "restfly",
    ],
)
