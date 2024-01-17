import math
import time
import tkinter
from random import random
from serial import Serial
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


ser = Serial("/dev/tty.usbmodem206B378239472", 115200)

def waitforstring():
    while True:
        if (ser.in_waiting != 0):
            bstring = ser.readline()
            bstring = bstring.strip()
            return bstring.decode("utf-8")
            break

def send_message(axes,canvas):


    try:
        
        # Send start message to microcontroller here
        #
        #
        #
        
        # Setup lists in which to store data points
        xvals = []
        yvals = []
        
        
    
        # Wait for data to be recieved from microcontroller
        print("PC - Waiting for Data Transfer...")
        while True:
            
            # Check for start message from microcontroller
            line = waitforstring()
            if (line == "Start Data Transfer"):
                break
            else:
                print("Microcontroller - " + line)
                continue
               
        # The first line should be the headers for plot axes
        firstLine = waitforstring()
        labels = firstLine.split(",")
        print("PC - Captured Header Line")
        
        # Wait for remaining data points to appear
        while True:
            # Read current line
            currentLine = waitforstring()
            
            # If the end block occurs, break
            if (currentLine != "End"):
                
                
                # Modify comma separated values to ensure uniformity
                
                # Strip any beginning/ending spaces
                #moddedline = line.strip()
                
                # Replace all spaces with commas
                moddedline = currentLine.replace(" ",",")
            
                # Split based on commas
                strings = moddedline.split(",")
                
                
                try:
                    # Convert to floating point numbers
                    xpt = float(strings[0])
                    ypt = float(strings[1])
                    
                    # Store only the first two data points            
                    xvals.append(xpt)
                    yvals.append(ypt)
                    
                except:
                    print("PC - Read Error on data: " + currentLine)
                    continue
            else:
                print("PC - End Data Transfer")
                break
            
            
        # Data transfer complete
        # Plot the data on the gui
        plot_data(axes, canvas, xvals, yvals, labels)
        
        
            
    except KeyboardInterrupt:
        print("Keyboard interrupt... Shutting Down")
        ser.close()
        print("Serial Closed")
        
    except Exception as e:
        # general purpose error handling
        print(e)
        ser.close()
        print("Serial Closed")
        
def plot_data(plot_axes, plot_canvas,xvals,yvals,labels):
    
    plot_axes.clear()
    plot_canvas.draw()
    print("PC - Plotting Data...")
    plot_axes.plot(xvals, yvals)
    plot_axes.set_xlabel(labels[0])
    plot_axes.set_ylabel(labels[1])
    plot_axes.grid(True)
    plot_canvas.draw()

def test(title):
    tk_root = tkinter.Tk()
    tk_root.wm_title(title)
    
    fig = Figure()
    axes = fig.add_subplot()
    # Create the drawing canvas and a handy plot navigation toolbar
    canvas = FigureCanvasTkAgg(fig, master=tk_root)
    toolbar = NavigationToolbar2Tk(canvas, tk_root, pack_toolbar=False)
    toolbar.update()
    
    
    toolbar = NavigationToolbar2Tk(canvas, tk_root, pack_toolbar=False)
    toolbar.update()
    
    button_run = tkinter.Button(master=tk_root, text="Run", command=lambda: send_message(axes, canvas))
    button_clear = tkinter.Button(master=tk_root,text="Clear",command=lambda: axes.clear() or canvas.draw())
    button_quit = tkinter.Button(master=tk_root, text="Quit", command=tk_root.destroy)
    
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)
    toolbar.grid(row=1, column=0, columnspan=3)
    button_run.grid(row=2, column=0)
    button_quit.grid(row=2, column=2)
    button_clear.grid(row=2, column=1)
    
    tkinter.mainloop()
    
if __name__ == "__main__":
    test(title = "test")