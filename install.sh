#!/usr/bin/env bash
# shellcheck disable=SC1090

# Remove any previous versions
sudo pip3 uninstall ip-lock -y

# Clone Repository
git clone https://github.com/chasenicholl/ip-lock.git

# Install Python Module
cd ip-lock && sudo python3 setup.py install

# Clean up
cd ../ && sudo rm -rf ./ip-lock
