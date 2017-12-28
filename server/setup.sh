#!/bin/bash

if [ ! -d "$DIRECTORY" ]; then
    sudo pip install virtualenv
    virtualenv -p /usr/bin/python2.7 venv
fi

. venv/bin/activate
which pip
pip install -r ./requirements.txt