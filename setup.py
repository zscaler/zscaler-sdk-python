import io
from setuptools import setup, find_packages


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

setup(name="zscaler-sdk-python",
      version='0.1.2',
      packages=find_packages(exclude=["tests", "*tests.*", "*tests"]),
      package_data=package_data,
      python_requires=">=3.8,<4.0",
      install_requires=["arrow", "certifi", "charset-normalizer", "idna", "python-box",
        "python-dateutil", "requests", "responses", "restfly", "six",
        "urllib3", "flatdict", "pyyaml", "xmltodict", "yarl",
        "pycryptodomex", "aenum", "pydash", "flake8", "pytz"],
      extras_require={"dev": ["black", "pytest", "pytest-asyncio", "pytest-mock", "pytest-recording",
                              "pytest-cov", "pyfakefs", "aenum", "isort", "wheel",
                              "pydash"]},
      author="Zscaler, Inc.",
      author_email="devrel@zscaler.com",
      description="Official Python SDK for the Zscaler Products (Beta)",
      long_description=io.open("README.md", encoding="utf-8").read(),
      long_description_content_type='text/markdown',
      url="https://zscaler-sdk-python.readthedocs.io",
      keywords="zscaler, sdk, zpa, zia, zdx, zcc, zcon",
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3.11",
          "Operating System :: OS Independent"])
