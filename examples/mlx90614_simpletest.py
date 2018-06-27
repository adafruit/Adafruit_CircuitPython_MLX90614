#  Designed specifically to work with the MLX90614 sensors in the
#  adafruit shop
#  ----> https://www.adafruit.com/products/1748
#  ----> https://www.adafruit.com/products/1749
#
#  These sensors use I2C to communicate, 2 pins are required to
#  interface Adafruit invests time and resources providing this open
#  source code,
#  please support Adafruit and open-source hardware by purchasing
#  products from Adafruit!

import board
import busio as io   
import adafruit_mlx90614

# use bitbangio only with ESP8266 
# * does not support hardware i2c
# * comment out busio above
# * express boards can use also bitbangio, but they have i2c hardware built-in
#import bitbangio as io 

# the mlx90614 must be run at 100k [normal speed]
# i2c default mode is is 400k [full speed] 
# the mlx90614 will not appear at the default 400k speed
i2c = io.I2C(board.SCL, board.SDA, frequency=100000) 
mlx = adafruit_mlx90614.MLX90614(i2c)

print("Ambent Temp: ", mlx.read_ambient_temp_f)
print("Object Temp: ", mlx.read_object_temp_f)
