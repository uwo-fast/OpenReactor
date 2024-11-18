#!/bin/bash

# Quit script if there are any errors
set -e

# Update all submodules
git submodule update --init --recursive

# Install needed dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-venv sqlite3 npm
sudo apt install -y libpq-dev python3-dev python-dev-is-python3
sudo apt install -y build-essential
sudo apt install -y postgresql-server-dev-all

# Create and configure python virtual environment
python3 -m venv .venv

# Ensure pip is installed in the virtual environment
source .venv/bin/activate
python3 -m ensurepip --upgrade

# Update permissions
sudo chmod -R a+rwx .venv

# Upgrade pip, setuptools, and wheel
pip install --upgrade pip setuptools wheel

# Install required Python packages
pip install -r requirements.txt
pip install --upgrade adafruit-blinka adafruit-platformdetect

# Install NPM packages
cd static || exit
npm install
