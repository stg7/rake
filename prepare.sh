#!/bin/bash
pyvenv --copies py
. py/bin/activate
cd py
hg clone https://bitbucket.org/pygame/pygame
cd pygame
python3 setup.py build
python3 setup.py install
#pip install numpy
