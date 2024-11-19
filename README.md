# OpenReactor

An easily extensible open source turbidostat with pH and dissolved oxygen control, written in python3.

# Installation

### For Ubuntu/Raspbian Systems

```sh
# Make sure git is installed
sudo apt install -y git

#Make sure node is installed
sudo apt install nodejs

# Clone and enter repository
git clone https://github.com/uwo-fast/openreactor
cd openreactor

# Run setup script
./first_time_setup.sh
```

## Running

```sh
./start.sh
```

## Updating

```sh
git pull --all
git submodule foreach git pull
```

## Reseting python enviroment when done running

```sh
deactivate
```

## Web Interface

The web interface can be accessed by any computer on the same network. If you're connecting from a computer on the local network, this is the ip of the address of the computer running the server followed by `:5000`, for example `141.219.193.214:5000`. If you're accessing it from the same computer that is running the server this is also `localhost:5000`

**Note** if youre unsure of the address, when launched the server will print the address that can be connected to in the console.

- ```* Running on http://141.219.193.214:5000/ (Press CTRL+C to quit)```

Setup
===

## Adding Devices

To add an I2C device/sensor to the system it it must be defined properly in <i>devices.json</i>.

<i>devices.json</i> contains two sections, "DEVICES" & "CONTROLS" any sensor needs to be added to "DEVICES" as well as any control mechanism that you also want to read from. I2C devices defined in "DEVICES" are read/read write. "CONTROLS" contains the information for any control system, and is write only.

**Note** connected devices are detected dynamically on launch, as such you can leave unused devices in *devices.json* but if a new device is added after the software is running the system must be rebooted.

An example of <i>devices.json</i>

```

{
"DEVICES":[
   {
      "name":"pH",
      "address":99,
      "unit":"pH",
      "form":"Atlas",
      "req_msg":82,
      "delay":0.9,
      "read_length":31
   },
   {
      "name":"Dissolved Oxygen",
      "address":100,
      "unit":"% Oxygen",
      "form":"Atlas",
      "req_msg":82,
      "delay":0.9,
      "read_length":31
   },
   {
      "name":"Adafruit Temperature Sensor",
      "address":25,
      "unit":"Degrees Celcius",
      "form":"temp_ada",
      "req_msg":5,
      "delay":0.0,
      "read_length":2
   },
   {
      "name":["Arduino Test I2C","Arduino Test I2C 2"],
      "address":97,
      "unit":["",""],
      "form":["byte","byte"],
      "req_msg":[[82,72],[]],
      "delay":[0.0,0.0],
      "read_length":[4,4]
   }
],
"CONTROLS":[
   {
      "name":["Control Test","Control Test 2"],
      "address":97,
      "unit":["",""],
      "form":["byte","byte"],
      "req_msg":[[82,72],54],
      "delay":[0.0,0.0],
      "read_length":[4,4],
      "enabled":[true,false],
      "params":[{
         "min":0,
         "max":0,
         "control":"control.demo"
      },
      {
         "min":0,
         "max":0,
         "control":"control.demo"
      }
   ],
      "def_state":[true,false]
   },
   {
      "name":"Control Test 3",
      "address":96,
      "unit":"",
      "form":"byte",
      "req_msg":[82,72],
      "delay":0.0,
      "read_length":4,
      "enabled":false,
      "params":{
         "min":0,
         "max":0,
         "target":100,
         "control":"control.demo"
      },
      "def_state":true
   }
]
}
```

In the "DEVICES" section
-

- "name" is the name given to the sensor, this must be unique.
- "address" is the I2C address of the sensor. "unit" is the unit of the measurement (can be an empty string but is required).
- "form" is how the recieved string is processed and must correlate to a section in <i>sensors/sensor_format.py </i>(see next section).
- "req_msg" is the message to send over I2C, can be a number or a list of numbers correlating to the I2C buffer. If no message is to be sent before the read, this can be left as an empty array: ```[]```.
- "delay" is the delay between the write and read required by some sensors.
- "read_length" is the number of bytes to read from the device.

**NOTE** that if multiple measurements need to be taken from a single device at one address every parameter must be given as a list except for the address (see "Arduino Test I2C", "Arduino Test I2C 2" in the example).

In the "CONTROLS" section
-

- "name" is the string that is used as a name for the control like in "DEVICES" this must be unique, but can have the same name as an item in "DEVICES".
- "address" the I2C address for the output, that means if you wanted to send a command to the pump board for example, you used the pump board address.
- "unit" the unit of the measurement, can just be empty string.
- "req_msg" the initial request message to be sent to I2C device, this is what is overwritten in this program so this is just an init
- "delay" the delay between read and write for sensors, this is not actually used for controls but is still required for parse
- "read_length" length of bytes to read, not actually used for controls but is still required for parse
- "enabled" this is legacy but I'm too lazy right now to fix it, these values are overwritten so don't really matter, must be binary

- "params : a sub-dictionary of custom parameters for each control system.
  - parameters must be a single integer to be parsed by interface at the moment but can have any number of parameters.  
  - **NOTE** that the only required parameter is "control" where in this case model.demo is the absolute path to the feedback mechanism .py file (control.demo is equivalent to control/demo.py).
- "def_state" the default state of the control systems, (on : true, off : false).

For "CONTROLS" in the first section two mechanisms are defined that will write to the same I2C address (in this case 97). This must be done in this manner and they cannot be listed seperately as you would for devices with seperate addresses.

# Received bytes Formatting

To process the recieved bytes into a parseable float/int/string an ```elif``` statement must be added to *sensor/sensor_format.py* where it's true condition correlates to the string given as "form" in *devices.json*

# Feedback Definition

To define the feedback for a control system a ```.py``` file with a path as defined in *devices.json* must be created.

- The Class must be named ```feedback```
- Must take the name of the control as an init argument
- Must return a byte string that is the commmand to send over I2C to the device specified in 'devices.json'
- Return must be from a function named *process* that does not take any required arguments
- Must have property self.outputType a string that contains the type of packing used for the byte, ie. 'f' for a float or 'b' for a signed char
- *reset* must be a function that resets the parameters to their default values

**NOTE** see *control/demo.py* for an example and more information

## Credits

Icons from [feathericons](https://feathericons.com)

Opensource logo from [Remix Icom](https://remixicon.com/)


# START OF DOCS

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
  - Control scripts in `control/` directory, e.g., `bread_heater_pid.py`, `ph_pid.py`, implementing specific control algorithms.
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
- **pid.py**: Implements a generic PID controller function used by other control scripts.
- **Control Scripts**:
  - **bread_heater_pid.py**: Controls a heater using PID based on temperature sensor feedback.
  - **ph_pid.py**: Controls pH levels by adjusting acid/base pumps using PID.
  - **bread_motor_i.py**, **bread_motor_ii.py**: Control scripts for motors.
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