import cqueue
import utime
import micropython
# Allocate memory to catch exceptions in interrupts
micropython.alloc_emergency_exception_buf(100)


"""! @file main.py
Doxygen style docstring for the file 
"""

QUEUE_SIZE = 200
int_queue = cqueue.IntQueue(QUEUE_SIZE)

adc = pyb.ADC(pyb.Pin.board.PB0)

doFillQueue = False

def timer_int(tim_num):
  """!
  Doxygen style docstring for interrupt callback function
  """
  #print("interrupting")
  if doFillQueue == True:
      int_queue.put(adc.read())


def step_response ():
    """!
    Doxygen style docstring for this function 
    """
    # Function code here
      
    # Setup Timer
    timmy = pyb.Timer(1, freq = 100)
    timmy.counter ()
    timmy.callback(timer_int)

    
    pinA5 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)

    pinA5.value(0)
    utime.sleep(3.0)
    pinA5.value(1)
    
    
    print("Capturing...")
    global doFillQueue
    doFillQueue = True
    print(doFillQueue)
    
    while int_queue.full() == False:
        # do nothing and wait
        ham = 0
        
    
    print("Capture Complete")
    doFillQueue = False
    
    i = 0;
    for num in range(QUEUE_SIZE):
        voltageRead = int_queue.get()/4096 * 3.3
        outString = str(i*10) + "," + str(voltageRead)
        i += 1
        print(outString)
        
    print("End");

if __name__ == "__main__":
  step_response()
