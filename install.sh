#!/usr/bin/env bash
# shellcheck disable=SC1090

# Clone Repository
git clone git@github.com:chasenicholl/ip-lock.git

# Install Python Module
cd ip-lock && python3 setup.py install

# Clean up
cd ../ && rm -rf ./ip-lock
