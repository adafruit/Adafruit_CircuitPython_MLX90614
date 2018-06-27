# The MIT License (MIT)
#
# Copyright (c) 2018 Mikey Sklar for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_mlx90614`
====================================================

CircuitPython module for the MLX90614 IR object temperature sensor.

* Author(s): Mikey Sklar based on code from these projects:
  Limor Fried - https://github.com/adafruit/Adafruit-MLX90614-Library
  Bill Simpson - https://github.com/BillSimpson/ada_mlx90614
  Mike Causer - https://github.com/mcauser/micropython-mlx90614

Implementation Notes
--------------------

**Hardware:**

* Sensors:
  https://www.adafruit.com/products/1748
  https://www.adafruit.com/products/1749

* Datasheet:
  https://cdn-shop.adafruit.com/datasheets/MLX90614.pdf

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
"""

from micropython import const

import adafruit_bus_device.i2c_device as i2c_device


# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/mikeysklar/Adafruit_CircuitPython_mlx90614.git"

#pylint: disable=bad-whitespace
# Internal constants:
_MLX90614_I2CADDR = const(0x5A)

# RAM
_MLX90614_RAWIR1 = const(0x04)
_MLX90614_RAWIR2 = const(0x05)
_MLX90614_TA = const(0x06)
_MLX90614_TOBJ1 = const(0x07)
_MLX90614_TOBJ2 = const(0x08)

# EEPROM
_MLX90614_TOMAX = const(0x20)
_MLX90614_TOMIN = const(0x21)
_MLX90614_PWMCTRL = const(0x22)
_MLX90614_TARANGE = const(0x23)
_MLX90614_EMISS = const(0x24)
_MLX90614_CONFIG = const(0x25)
_MLX90614_ADDR = const(0x0E)
_MLX90614_ID1 = const(0x3C)
_MLX90614_ID2 = const(0x3D)
_MLX90614_ID3 = const(0x3E)
_MLX90614_ID4 = const(0x3F)
#pylint: enable=bad-whitespace

class MLX90614:
    """Create an instance of the MLX90614 temperature sensor.  You must pass in
    the following parameters:
    - i2c: An instance of the I2C bus connected to the sensor.
    - frequency=100000 - this sensor does not respond to the default 400000 i2c bus speed

    Optionally you can specify:
    - address: The I2C address of the sensor.  If not specified the sensor's
               default value will be assumed.
    """

    def __init__(self, i2c_bus, address=_MLX90614_I2CADDR):
        self._device = i2c_device.I2CDevice(i2c_bus, address)
        self.buf = bytearray(2) 
        self.buf[0] = _MLX90614_CONFIG

    @property
    def read_ambient_temp_f(self):
        """Ambient Temperature in fahrenheit.""" 
        return ( ( self._read_temp(_MLX90614_TA) * 9/5 ) + 32)

    @property
    def read_object_temp_f(self):
        """Object Temperature in fahrenheit.""" 
        return ( ( self._read_temp(_MLX90614_TOBJ1) * 9/5 ) + 32)

    @property
    def read_ambient_temp_c(self):
        """Ambient Temperature in celsius.""" 
        return ( self._read_temp(_MLX90614_TA) )

    @property
    def read_object_temp_c(self):
        """Object Temperature in celsius.""" 
        return ( self._read_temp(_MLX90614_TOBJ1) )

    def _read_temp(self, register):
        temp = self._read_16(register)
        temp *= 0.02
        temp -= 273.15
        return (temp)

    def _read_16(self, register):
        # Read and return a 16-bit unsigned big endian value read from the
        # specified 16-bit register address.
        with self._device:
            self.buf[0] = register
            self._device.write(self.buf, end=1, stop=False)
            self._device.readinto(self.buf)
            return ( self.buf[1] << 8 | self.buf[0] )
