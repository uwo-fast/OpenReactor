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

- `* Running on http://141.219.193.214:5000/ (Press CTRL+C to quit)`

# Setup

## Adding Devices

To add an I2C device/sensor to the system it it must be defined properly in <i>devices.json</i>.

<i>devices.json</i> contains two sections, "DEVICES" & "CONTROLS" any sensor needs to be added to "DEVICES" as well as any control mechanism that you also want to read from. I2C devices defined in "DEVICES" are read/read write. "CONTROLS" contains the information for any control system, and is write only.

**Note** connected devices are detected dynamically on launch, as such you can leave unused devices in _devices.json_ but if a new device is added after the software is running the system must be rebooted.

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
         "control":"controls.demo"
      },
      {
         "min":0,
         "max":0,
         "control":"controls.demo"
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
         "control":"controls.demo"
      },
      "def_state":true
   }
]
}
```

## In the "DEVICES" section

- "name" is the name given to the sensor, this must be unique.
- "address" is the I2C address of the sensor. "unit" is the unit of the measurement (can be an empty string but is required).
- "form" is how the recieved string is processed and must correlate to a section in <i>sensors/sensor_format.py </i>(see next section).
- "req_msg" is the message to send over I2C, can be a number or a list of numbers correlating to the I2C buffer. If no message is to be sent before the read, this can be left as an empty array: `[]`.
- "delay" is the delay between the write and read required by some sensors.
- "read_length" is the number of bytes to read from the device.

**NOTE** that if multiple measurements need to be taken from a single device at one address every parameter must be given as a list except for the address (see "Arduino Test I2C", "Arduino Test I2C 2" in the example).

## In the "CONTROLS" section

- "name" is the string that is used as a name for the control like in "DEVICES" this must be unique, but can have the same name as an item in "DEVICES".
- "address" the I2C address for the output, that means if you wanted to send a command to the pump board for example, you used the pump board address.
- "unit" the unit of the measurement, can just be empty string.
- "req_msg" the initial request message to be sent to I2C device, this is what is overwritten in this program so this is just an init
- "delay" the delay between read and write for sensors, this is not actually used for controls but is still required for parse
- "read_length" length of bytes to read, not actually used for controls but is still required for parse
- "enabled" this is legacy but I'm too lazy right now to fix it, these values are overwritten so don't really matter, must be binary

- "params : a sub-dictionary of custom parameters for each control system.
  - parameters must be a single integer to be parsed by interface at the moment but can have any number of parameters.
  - **NOTE** that the only required parameter is "control" where in this case model.demo is the absolute path to the feedback mechanism .py file (controls.demo is equivalent to control/demo.py).
- "def_state" the default state of the control systems, (on : true, off : false).

For "CONTROLS" in the first section two mechanisms are defined that will write to the same I2C address (in this case 97). This must be done in this manner and they cannot be listed seperately as you would for devices with seperate addresses.

# Received bytes Formatting

To process the recieved bytes into a parseable float/int/string an `elif` statement must be added to _sensor/sensor_format.py_ where it's true condition correlates to the string given as "form" in _devices.json_

# Feedback Definition

To define the feedback for a control system a `.py` file with a path as defined in _devices.json_ must be created.

- The Class must be named `feedback`
- Must take the name of the control as an init argument
- Must return a byte string that is the commmand to send over I2C to the device specified in 'devices.json'
- Return must be from a function named _process_ that does not take any required arguments
- Must have property self.outputType a string that contains the type of packing used for the byte, ie. 'f' for a float or 'b' for a signed char
- _reset_ must be a function that resets the parameters to their default values

**NOTE** see _control/demo.py_ for an example and more information

## Credits

Icons from [feathericons](https://feathericons.com)

Opensource logo from [Remix Icom](https://remixicon.com/)
