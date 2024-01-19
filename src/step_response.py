"""! @file main.py
This program runs a 3.3V step on output pin A5, and then records
the immediate response on pin PB0 for the following 2 seconds.
Data points from the recorded response are printed over serial.
"""

import cqueue
import utime
import micropython
import pyb

# Allocate memory to catch exceptions in interrupts
micropython.alloc_emergency_exception_buf(100)

# Setup queue for optimized data storage in an interrupt
QUEUE_SIZE = 200
int_queue = cqueue.IntQueue(QUEUE_SIZE)

# Enable adc pin
adc = pyb.ADC(pyb.Pin.board.PB0)


def timer_int(tim_num):
  """!
  This timer interrupt runs every 10ms.
  Fills queue with ADC value every pass through.
  """
  int_queue.put(adc.read())


def step_response ():
    """!
    This function sets up the timer interrupt and output pin.
    It then pauses breifly before performing the step input and capturing data. Data capture is complete when the queue is full.
    """
    # Function code here

    # First Time setup:
    #Setup output pin
    pinA5 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)
    
    try:

    
        # Temporary Pullup to start
        
#             print("Waiting for button start...")
#             startAdc = pyb.ADC(pyb.Pin.board.PA0)
#             while True:
#                 if startAdc.read() < 2000:
#                     # Start code
#                     print(startAdc.read())
#                     break
#                 else:
#                     continue
#                 

        # Set output pin to 0, and allow all transient response to settle before performing the step input
        pinA5.value(0)
        utime.sleep(3.0)
        pinA5.value(1)
        
        # Begin capturing data by enabling interrupt and callbacks
        timmy = pyb.Timer(1, freq = 100)
        timmy.counter ()
        timmy.callback(timer_int)
        print("Capturing...")
        
        while int_queue.full() == False:
            # Do nothing and wait for queue to fill
            continue
        
        # Once complete, halt callbacks so that the queue does not get overwritten
        timmy.callback(None)
        # Turn off the trigger pin
        pinA5.value(0)
        
        print("Capture Complete")
        print("Start Data Transfer")
        print("Time [s], Voltage [V]")
        # Loop over data collected in queue
        for i in range(QUEUE_SIZE):
            # Map adc values to voltage
            voltageRead = int_queue.get()/4096 * 3.3
            # Create the string to print using csv format
            outString = str(i*10) + "," + str(voltageRead)
            print(outString)
            
        print("End");
    
    except KeyboardInterrupt:
            print("PROGRAM INTERRUPTED")
            # Turn off trigger pin
            pinA5.value(0)

if __name__ == "__main__":
  step_response()

