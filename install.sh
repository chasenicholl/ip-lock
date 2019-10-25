#!/usr/bin/env bash
# shellcheck disable=SC1090

# Clone Repository
git clone https://github.com/chasenicholl/ip-lock.git

# Install Python Module
cd ip-lock && sudo python3 setup.py install

# Clean up
cd ../ && sudo rm -rf ./ip-lock
