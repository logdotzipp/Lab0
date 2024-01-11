import cqueue
import utime
import micropython
# Allocate memory to catch exceptions in interrupts
micropython.alloc_emergency_exception_buf(100)


"""! @file main.py
   This program runs a 3.3V step on output pin A5, and then records the immediate response on pin PB0 for the following 2 seconds. Data points from the recorded response are printed over serial.
"""

# Setup queue for optimized data storage in an interrupt
QUEUE_SIZE = 200
int_queue = cqueue.IntQueue(QUEUE_SIZE)

# Enable adc pin
adc = pyb.ADC(pyb.Pin.board.PB0)

# Initialize doFillQueue to prevent the queue from filling immediately
doFillQueue = False

def timer_int(tim_num):
  """!
  This timer interrupt runs every 10ms. It only fills the queue with data when doFillQueue is set to true.
  """
  #print("interrupting")
  if doFillQueue == True:
      int_queue.put(adc.read())


def step_response ():
    """!
    This function sets up the timer interrupt and output pin. It then pauses breifly before performing the step input and capturing data. Data capture is complete when the queue is full.
    """
    # Function code here
      
    # Setup Timer
    timmy = pyb.Timer(1, freq = 100)
    timmy.counter ()
    timmy.callback(timer_int)

    # Setup output pin
    pinA5 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)

    # Set output pin to 0, and allow all transient response to settle before performing the step input
    pinA5.value(0)
    utime.sleep(3.0)
    pinA5.value(1)
    
    
    # Begin capturing data by enabling doFillQueue
    print("Capturing...")
    global doFillQueue
    doFillQueue = True
    print(doFillQueue)
    
    
    while int_queue.full() == False:
        # do nothing and wait for queue to fill
        ham = 0
        
    
    print("Capture Complete")
    # Prevent the queue from being overwritten
    doFillQueue = False
    
    
    # Loop over data collected in queue
    for i, num in range(QUEUE_SIZE):
        # Map adc values to voltage
        voltageRead = int_queue.get()/4096 * 3.3
        # Create the string to print using csv format
        outString = str(i*10) + "," + str(voltageRead)
        print(outString)
        
    print("End");

if __name__ == "__main__":
  step_response()

