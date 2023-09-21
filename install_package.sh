#!/bin/bash

rm -rf dist
rm -rf zscaler_sdk_python.egg-info
python setup.py sdist
pip3 install dist/zscaler-sdk-python-1.0.0.tar.gz
