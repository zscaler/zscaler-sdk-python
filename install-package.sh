#!/usr/bin/env bash

rm -rf dist
rm -rf zscaler_sdk_python.egg-info
pip3 install -r dev_requirements.txt
# pip3 install -r requirements.txt
python3 setup.py sdist
pip3 install dist/zscaler-sdk-python-1.0.0.tar.gz
