# Bioreactor Control and Monitoring System

This project is a software application designed to run on a Raspberry Pi to control and monitor a bioreactor system. It interfaces with various sensors and control devices over the I2C bus to perform experiments and manage the bioreactor environment.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Components](#components)
  - [Sensor Module](#sensor-module)
  - [Control Module](#control-module)
  - [Web Interface](#web-interface)
  - [Experiment Management](#experiment-management)
- [Key Files and Directories](#key-files-and-directories)
  - [app.py](#apppy)
  - [cycle.py](#cyclepy)
  - [sensor/](#sensor-directory)
  - [control/](#control-directory)
  - [experiments/](#experiments-directory)
  - [templates/ and static/](#templates-and-static-directories)
  - [start.sh](#startsh)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Setup and Installation](#setup-and-installation)
- [Notes](#notes)

## Overview

The application allows for real-time monitoring and control of a bioreactor by communicating with various I2C devices connected to a Raspberry Pi. It includes a web interface for user interaction, data visualization, and experiment management.

## Architecture

The system is composed of several modules:

- **Sensor Module**: Handles data acquisition from sensors.
- **Control Module**: Manages actuators and control mechanisms.
- **Web Interface**: Provides a user interface for monitoring and controlling the bioreactor.
- **Experiment Management**: Allows for starting, stopping, and managing experiments.
- **Data Storage**: Uses a SQLite database to store sensor readings and control statuses.

## Components

### Sensor Module

- **Description**: Interfaces with I2C sensors to read measurements such as temperature, pH, etc.
- **Key Classes**:
  - `I2C` in `sensor.py`: Represents an I2C device, capable of reading data and storing it in the database.
- **Functionality**:
  - Auto-detection of connected sensors via `device_detect.py`.
  - Data formatting and calibration using `sensor_format.py` and calibration equations.
  - Storage of sensor readings in a SQLite database using Peewee ORM.

### Control Module

- **Description**: Controls actuators like pumps, heaters, and motors to manage the bioreactor environment.
- **Key Classes and Scripts**:
  - Control scripts in `control/` directory, e.g., `BREADheaterPID.py`, `phPID.py`, implementing specific control algorithms.
  - `feedback` classes implement control logic and algorithms (e.g., PID control).
- **Functionality**:
  - Real-time control based on sensor feedback.
  - Customizable control parameters and algorithms defined in `devices.json`.

### Web Interface

- **Description**: A Flask-based web application that provides a UI for users to interact with the system.
- **Key Features**:
  - Dashboard displaying real-time sensor data.
  - Control panel to adjust control parameters and enable/disable controls.
  - Graphs for data visualization of sensor readings over time.
  - Experiment management (start, stop, create, delete experiments).

### Experiment Management

- **Description**: Manages experiments by recording start and end times and associating sensor data with specific experiments.
- **Functionality**:
  - Create new experiments and store metadata in JSON files within the `experiments/` directory.
  - Start and stop experiments, triggering data acquisition threads.
  - Retrieve data associated with specific experiments for analysis and export.

## Key Files and Directories

### app.py

- **Description**: The main Flask application that runs the web server and handles routing.
- **Key Functions**:
  - Initializes sensor (`I2C_dev`) and control (`I2C_con`) devices.
  - Manages threading for data acquisition (`experimentThreadStart`, `experimentThreadStop`).
  - Provides routes for web pages and AJAX calls for dynamic updates (`/graphs`, `/controls`, `/update/controls`, etc.).
- **Highlights**:
  - Uses threading to perform sensor reads at defined intervals without blocking the web server.
  - Interacts with the database to store and retrieve sensor readings and control statuses.
  - Implements experiment lifecycle management.

### cycle.py

- **Description**: Contains the `experimentCycle` class, which is a placeholder for managing experiment cycles.
- **Functionality**:
  - Manages multiprocessing for experiment cycles (currently a stub for future implementation).

### sensor/ Directory

- **sensor.py**: Defines the `I2C` class for interacting with sensors and actuators over I2C.
  - Capable of reading sensor data, formatting it, and storing it in the database.
  - Handles both sensor readings and control messages.
- **sensor_format.py**: Contains the `form` function for formatting raw sensor data based on specified formats.
- **device_detect.py**: Detects connected I2C devices based on configurations in `devices.json`.
  - Separates devices into sensors (`devs`) and controls (`cons`).
- **maths/**:
  - **symbolicParser.py**: Parses calibration equations for sensor data (e.g., linear transformations).
  - **equations.json**: Stores calibration equations for each sensor.

### control/ Directory

- Contains control scripts implementing specific control algorithms.
- **PID.py**: Implements a generic PID controller function used by other control scripts.
- **Control Scripts**:
  - **BREADheaterPID.py**: Controls a heater using PID based on temperature sensor feedback.
  - **phPID.py**: Controls pH levels by adjusting acid/base pumps using PID.
  - **BREADmotor_I.py**, **BREADmotor_II.py**: Control scripts for motors.
  - **demo.py**: An example control script demonstrating how to implement a feedback mechanism.

### experiments/ Directory

- **experiments.py**: Manages experiment configurations and status.
  - Handles creation, starting, stopping, and deletion of experiments.
  - Stores experiment metadata in JSON files within the `experiments/` directory.

### templates/ and static/ Directories

- **templates/**: Contains HTML templates for the web interface using Flask's templating engine (Jinja2).
  - **index.html**: The main landing page.
  - **graphs.html**: Displays graphs of sensor data.
  - **controls.html**: Provides control interfaces for actuators.
  - **about.html**: Information about the application.
- **static/**: Contains static files like CSS, JavaScript, and images.
  - **package.json** and **package-lock.json**: For managing frontend dependencies (if any).

### start.sh

- **Description**: A shell script to start the Flask web server.
- **Usage**:
  - Activates the Python virtual environment.
  - Sets required environment variables (`FLASK_APP`, `FLASK_ENV`).
  - Runs the Flask application with `--no-reload` to prevent multiple threads from spawning.

### model.py

- **Description**: Defines the database models using Peewee ORM.
- **Key Classes**:
  - `Sensor`: Represents a sensor device.
  - `SensorReading`: Stores readings from sensors.
  - `Control`: Represents a control device.
  - `ControlReading`: Stores control actions and statuses.
  - `systemSettings`: Stores system-wide settings (e.g., cycle length).
- **Functionality**:
  - Provides a `Data` class as a data access layer for database interactions.

## Usage

1. **Start the Application**:
   - Run the `start.sh` script: `./start.sh`.
   - Alternatively, manually start the Flask app by setting environment variables and running `flask run`.

2. **Access the Web Interface**:
   - Open a web browser and navigate to `http://<raspberry_pi_ip>:5000`.

3. **Monitor Sensors**:
   - View real-time sensor data on the dashboard.
   - Use the graphs page to visualize historical data.

4. **Control Actuators**:
   - Adjust control parameters and enable or disable controls via the controls page.

5. **Manage Experiments**:
   - Create new experiments, start or stop data acquisition, and download data.

## Dependencies

- **Python Packages** (as specified in `requirements.txt`):
  - Flask
  - Peewee (ORM for SQLite)
  - BusIO and Board (for I2C communication)
  - Other packages as required by the control scripts and web interface.
- **Hardware**:
  - Raspberry Pi with I2C-enabled sensors and actuators connected.

## Setup and Installation

1. **Enable I2C on Raspberry Pi**:
   - Use `sudo raspi-config` to enable the I2C interface.

2. **Install Required Python Packages**:
   - Create a virtual environment: `python3 -m venv .venv`
   - Activate the virtual environment: `source .venv/bin/activate`
   - Install packages: `pip install -r requirements.txt`

3. **Configure Devices**:
   - Define connected sensors and controls in `devices.json`.
   - Ensure the correct I2C addresses and parameters are specified.

4. **Database Initialization**:
   - The database `openreactor.db` will be automatically created and managed by Peewee ORM.

5. **Run the Application**:
   - Execute `./start.sh` to start the Flask web server.

6. **Access the Web Interface**:
   - Navigate to `http://<raspberry_pi_ip>:5000` in a web browser.

## Notes

- **Threading**:
  - The application uses threading to handle sensor readings and control actions at defined intervals without blocking the main web server.
  - Data acquisition runs in a separate thread managed by `experimentThreadStart` and `experimentThreadStop` functions in `app.py`.

- **Calibration**:
  - Calibration equations for sensors are stored in `sensor/maths/equations.json`.
  - Equations are applied to raw sensor data to calibrate readings.

- **Data Storage**:
  - Sensor readings and control statuses are stored in a SQLite database `openreactor.db`.
  - The database schema is defined in `model.py` using Peewee ORM.

- **Experiment Lifecycle**:
  - Experiments are managed via JSON files in the `experiments/` directory.
  - Starting an experiment initiates data acquisition; stopping an experiment halts data collection.
  - Multiple experiments can be managed, but only one can be running at a time due to threading.

- **Control Mechanisms**:
  - Control scripts must follow a specific structure, implementing a `feedback` class with a `process` method.
  - Control parameters are stored in the database and can be modified via the web interface.
  - Control devices send commands over I2C to actuators based on sensor feedback.

- **Web Interface**:
  - Uses AJAX calls to update sensor data and control statuses without refreshing the page.
  - Provides interactive graphs using data fetched from the server.

- **Logging and Error Handling**:
  - The application includes print statements and exception handling to aid in debugging.
  - Errors during sensor reads or control actions are logged to the console.