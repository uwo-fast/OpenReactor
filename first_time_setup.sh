#!/bin/bash

# Quit script if there are any errors
set -e

# Update all submodules
git submodule update --init --recursive

# Install needed dependancies
sudo apt update; sudo apt upgrade -y
sudo apt install -y python3-venv sqlite3 npm
sudo apt install libpq-dev python3-dev
sudo apt install build-essential
sudo apt install postgresql-server-dev-all

# Create and configure python virtual enviroment
python3 -m venv .venv
sudo chmod -R a+rwx .venv
source .venv/bin/activate
pip install wheel
pip install --upgrade wheel
pip install --upgrade setuptools
pip install -r requirements.txt

# Install NPM packages
cd static
npm i 
