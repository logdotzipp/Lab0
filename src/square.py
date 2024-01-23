"""! @file square.py
This program outputs a square wave with a period of 5 seconds
to the microcontroller.
"""
import utime

adc = pyb.ADC(pyb.Pin.board.PB0)
pinA5 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)

while True:
    pinA5.value(0)
    utime.sleep(5.0)
    pinA5.value(1)
    utime.sleep(5.0)