#!/bin/bash

# Source the python enviroment
source .venv/Scripts/activate

# Export the required enviroment variables
export FLASK_APP=app;
export FLASK_ENV=development;

# Run the web interface
flask run --host=0.0.0.0
