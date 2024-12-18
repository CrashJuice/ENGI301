# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
groove water level sensor driver
--------------------------------------------------------------------------
License:   
Copyright 2024 Juan Aizprua

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
This file provides an interface to a PWM controllered buzzer.
  - Ex:  https://www.adafruit.com/product/1536


APIs:
 - read_sensor_data recieves raw information from sensor
 - calculate_water_level calulates the water level as a percentage of total surface
 -get_water_level combines it all and returns water level

"""







import time
import smbus

# Constants
LOW_SENSOR_ADDR = 0x77  # I2C address of the lower-level sensor
HIGH_SENSOR_ADDR = 0x78  # I2C address of the higher-level sensor
THRESHOLD = 100  # Threshold for determining water level
SENSORVALUE_MIN = 250  # Minimum sensor value for a valid touch
SENSORVALUE_MAX = 255  # Maximum sensor value for a valid touch

# Initialize I2C bus
bus = smbus.SMBus(1)  # Use I2C bus 1 (default for BeagleBone)

def read_sensor_data():
    """Reads data from both the lower-level and higher-level sensors."""
    try:
        # Read from the lower-level sensor
        low_data = bus.read_i2c_block_data(LOW_SENSOR_ADDR, 0, 8)  # 8 bytes
        # Read from the higher-level sensor
        high_data = bus.read_i2c_block_data(HIGH_SENSOR_ADDR, 0, 12)  # 12 bytes

        # Combine both sensor data (8 bytes from low and 12 bytes from high)
        data = low_data + high_data

        if len(data) != (8 + 12):
            raise ValueError("Failed to read the expected number of bytes.")

        return data
    except Exception as e:
        print(f"Error reading sensor data: {e}")
        return None

def calculate_water_level(data):
    """Calculates the water level percentage based on the combined data from both sensors."""
    touch_val = 0  # Initialize the touch value (binary representation of water level)
    num_sections = len(data)  # Total number of sections from both sensors

    # Process each byte of data
    for i in range(num_sections):
        if data[i] > THRESHOLD:  # If data exceeds threshold, mark the section as touched
            touch_val |= 1 << i  # Set the corresponding bit in touch_val

    # Calculate which section is touched
    trig_section = 0
    while touch_val & 0x01:
        trig_section += 1
        touch_val >>= 1

    # Water level as a percentage based on the combined sections
    water_level = trig_section * (100 / num_sections)
    return water_level

def get_water_level():
    """Gets the water level percentage by reading data and calculating it from both sensors."""
    try:
        data = read_sensor_data()  # Read data from both sensors
        if data is None:
            return None
        water_level = calculate_water_level(data)  # Calculate water level percentage
        return water_level
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    while True:
        water_level = get_water_level()  # Get the water level
        if water_level is not None:
            print(f"Water level: {water_level:.2f}%")
        else:
            print("Failed to get water level.")
        
        time.sleep(1)  # Delay between readings
