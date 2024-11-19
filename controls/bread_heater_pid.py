import struct
from database.model import SensorReading, ControlReading
from controls.pid import pid


class feedback:
    def __init__(self, name, I2C):
        self.data = 0
        self.params = {}
        self.name = name
        self.I2C = I2C
        self.outputType = "b"
        self.identifier = 72  # Heater identifier

    def getData(self):
        self.getParams()
        try:
            thermocouple_number = self.params.get("thermocouple", 1)
            setpoint = float(self.params["setpoint"])
            kp = float(self.params["kp"])
            ki = float(self.params["ki"])
            kd = float(self.params["kd"])
            er = float(self.params.get("er", 0))

            # Get current and last input values
            input_value = float(
                SensorReading.select()
                .where(SensorReading.name == f"Thermo {thermocouple_number}")
                .order_by(SensorReading.id.desc())
                .get()
                .value
            )
            last_input = float(
                SensorReading.select()
                .where(SensorReading.name == f"Thermo {thermocouple_number}")
                .order_by(SensorReading.id.desc())
                .limit(2)[-1]
                .value
            )

            # Perform PID calculation
            output, er = pid(input_value, last_input, setpoint, kp, ki, kd, er=er)

            # Update parameters with new error term
            self.params["er"] = er
            self.data = output

        except Exception as e:
            print(f"Error in PID calculation for {self.name}: {e}")
            self.data = 0

    def getParams(self):
        try:
            self.params = (
                ControlReading.select()
                .where(ControlReading.name == self.name)
                .order_by(ControlReading.time.desc())
                .get()
                .params
            )
        except Exception as e:
            print(f"Error retrieving parameters for {self.name}: {e}")
            self.params = {}

    def params2data(self):
        try:
            # Pack the identifier and output data into bytes
            id_byte = struct.pack(self.outputType, self.identifier)
            data_byte = struct.pack(self.outputType, int(self.data))
            self.data = id_byte + data_byte
        except Exception as e:
            print(f"Error packing data for {self.name}: {e}")
            self.data = b""

    def process(self):
        self.getData()
        self.params2data()
        self.I2C.edit_params(self.params)
        output = self.data
        return output

    def reset(self):
        try:
            default_params = (
                ControlReading.select()
                .where(ControlReading.name == self.name)
                .order_by(ControlReading.time.asc())
                .get()
                .params
            )
            self.params = default_params
            id_byte = struct.pack(self.outputType, self.identifier)
            zero_byte = struct.pack(self.outputType, 0)
            return id_byte + zero_byte
        except Exception as e:
            print(f"Error resetting {self.name}: {e}")
            return b""
