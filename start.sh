#!/bin/bash

# Source the python enviroment
source .venv/bin/activate

# Export the required enviroment variables
export FLASK_APP=app;
export FLASK_ENV=development;

# Run the web interface --no-reload is needed as the app restarts the thread if it's meant to be open on launch, but restart causes two threads to spawn. 
flask run --host=0.0.0.0 --no-reload
