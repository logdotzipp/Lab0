import math
import time
import tkinter
from random import random
from serial import Serial
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

def waitforstring():
    while True:
        if (ser.in_waiting != 0):
            return ser.readline()
            break

def send_message():
    ser = Serial("/dev/tty.usbmodem206B378239472", 9600)
    
    ser.write("Start")
    
    while True:
         line = waitforstring()
         print(line)
#             # Split string so that it can be read
#             
#             # Check for second start block
#             if (line == "Start Data Transfer"):
#                 header = waitforstring()
#                 
#                 while True:
#                     if (waitforstring() != "End"):
#                         # Split and store values as plot points/labels
#                     else:
#                         break
#             else:
#                 print(line)
#                 continue
        
    

def test(title):
    tk_root = tkinter.Tk()
    tk_root.wm_title(title)
    
    fig = Figure()
    axes = fig.add_subplot()
    # Create the drawing canvas and a handy plot navigation toolbar
    canvas = FigureCanvasTkAgg(fig, master=tk_root)
    toolbar = NavigationToolbar2Tk(canvas, tk_root, pack_toolbar=False)
    toolbar.update()
    canvas = FigureCanvasTkAgg(fig, master=tk_root)
    
    toolbar = NavigationToolbar2Tk(canvas, tk_root, pack_toolbar=False)
    toolbar.update()
    
    button_run = tkinter.Button(master=tk_root, text="Print Message", command=lambda: send_message())
    
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)
    toolbar.grid(row=1, column=0, columnspan=3)
    button_run.grid(row=2, column=0)
    
    tkinter.mainloop()
    
if __name__ == "__main__":
    test(title = "test")