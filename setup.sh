#!/bin/bash

echo making sure we have pip3 and venv
if [ -x $pip3 ]
then
    echo setting up virtualenv if not already present
else
    echo it was not installed, probably installing
    sudo apt install python3-pip
fi

sudo apt install python3-venv

if [ -d odk2odm_venv ]
then
    echo venv was already present, hope it is the right one
else
    python3 -m venv odk2odm_venv
fi

echo creating and activating virtual environment
pip3 install wheel
pip3 install virtualenv
source odk2odm_venv/bin/activate
pip3 install wheel

echo installing odk2odm library and dependencies
pip install .

echo Done.
echo To use the utilities here, activate the virtual environment with:
echo source odk2odm_venv/bin/activate
echo
echo And type deactivate to get out when you are done.
