#This module was inspired  by this website:
#http://electronut.in/plotting-real-time-data-from-arduino-using-python/

"""The module is the main interface with
classes and a main method to implement an 
arduino based oscilloscope"""

#import the necessary packages and modules
import serial # python's serial communiation package
import numpy as np # numerical processing package
from collections import deque # data structure to store serial data
import matplotlib.pyplot as plt # 2D graphing package
from random import random   #random signal generator for testing
"""Objects of type ChannelData hold 
and manage data for the two channel oscilloscope"""

class ChannelData:
    #construct with maximum length as parameter
    def __init__(self, maxLen):
        self.maxLen = maxLen
        self.reset(1) #reset the channels(use empty deque)
        self.reset(2)

    def reset(self, channel):
        """Resets the particular channel
        Only channel 1 and 2 are available
        """
        if(channel == 1):
            #assign a double queue of maxLen with all elements 0
            self.channel1 = deque([0.0]*self.maxLen)
        if(channel == 2):
            self.channel2 = deque([0.0]*self.maxLen)

    def addToBuf(self,buf,val):
        #Handles adding new data to channels
        buf.pop()   #old data is removed from the right
        buf.appendleft(val)  #new data is appended to the left

    def add(self, data, toggle):
        """Add channel data
        data should be an array, where data[0] is data
        data from channel 1 and data[1] is data from channel 2.
        Toggle is an array of booleans that indicate whether the
        data from the corresponding channel should be added to the 
        data structure. (Used to implement channel off in oscilloscopes) 
        """
        if(toggle[0]):  #if channel 1 is on
            self.addToBuf(self.channel1,data[0])
        else:
            self.reset(1)
        if(toggle[1]):
            self.addToBuf(self.channel2,data[1])
        else:
            self.reset(2)

"""Objects of type ChannelPlot 
Handle plotting of oscilloscope data
using matplotlib. 
"""
class ChannelPlot:
    ylim = [-5,5]  #default vertical range
    xlim = [0,110] #visible horizontal range in points
                   #related with horizontal sweep
    div = 2   #initial volts per division
    divx = 4  #initial seconds per division
    current = 1 #'zoom in' factor for vertical scale
    currentx = 1 #'zoom in' factor for horizontal scale
    division = [1,2,4,8]  #available vertical zoom-levels 
    divisionx = [1,2,4,8] #available horizontal zoom-levels
    #horizontal zoom ranges in points
    xlims = [[0,110],[0,110.0/2],[0,110.0*1/4],[0,110.0*1/8]]

    #constructor takes instance of channel data
    def __init__(self,ChannelData):
        """Create ChannelPlot from a channelData object"""
        x = np.linspace(0,110,1000)
        plt.ion()  #interactive plotting
        #data curves for channel 1 and 2
        self.ch1, = plt.plot(x,ChannelData.channel1)
        self.ch2, = plt.plot(x,ChannelData.channel2)

        plt.legend([self.ch1,self.ch2],["Channel 1","Channel 2"])
        #limit the vertical and horizontal range in view
        plt.ylim(self.ylim)
        plt.xlim(self.xlim)

        plt.grid()   #enable oscilloscope grid like look
        plt.gca().axes.xaxis.set_ticklabels([])  # disable axes labels
        plt.gca().axes.yaxis.set_ticklabels([])
        plt.gcf().canvas.set_window_title('Oscilloscope')  # title

        plt.ylabel(str(self.div)+"V per divison")
        plt.xlabel(str(self.divx)+"s per division")
        plt.draw() #draw the scope

    def update(self,ChannelData, trigger):
        """Update plot with ChannelData object

        The trigger value is boolean. If it is enabled
        the signal is frozen. Technically this unrelated
        to the oscilloscope's trigger, but can be Used
        to get snapshots of the signal
        """
        if(trigger): #don't update if trigger is enabled
            return
        self.ch1.set_ydata(ChannelData.channel1)
        self.ch2.set_ydata(ChannelData.channel2)
        plt.draw()

    def zoom_Handle(self,level):
        """Handles vertical and horizontal sensitivity

        level is an array containing zoom data from arduino.
        """
        ver = level[0]  #vertical control
        hor = level[1]  #horizontal control
        #split inputs in range 0-1023 to 4
        #may result in erratic behavior at crossing points
        divider = self.division[ver/256]  
        dividerx = self.divisionx[hor/256]

        if(divider == self.current): #if zoom level not changed
            pass
        else:
            self.current = divider
            self.div = 2.0/divider #votls per division
            self.ylim[0] = -5.0/divider
            self.ylim[1] = 5.0/divider
            plt.ylabel(str(self.div)+"V per divison")
            plt.ylim(self.ylim)
        #do similar analysis for horizontal zoom
        if(dividerx == self.currentx):
            pass
        else:
            self.currentx = dividerx
            self.divx = 4.0/dividerx  #secs per division
            self.xlim = self.xlims[hor/256] #pick the appropriate range
            plt.xlabel(str(self.divx)+"s per divison")
            plt.xlim(self.xlim)

#main program
def main():
    #This are the list of serial ports used on my Ubuntu laptop
    #You may need to change this list if you're using a mac or Windows.
    #The particular serial port in use is indicated by arduino's ide
    strPorts = ['/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyACM2', '/dev/ttyACM3']
    channelData = ChannelData(1000)  
    channelPlot = ChannelPlot(channelData)
    ser = None  #variable to hold serial port
    #try connecting to a serial port
    for strPort in strPorts:
        try:
            #create a serial port object
            ser = serial.Serial(strPort,9600) 
        except Exception:
            pass
    #quit if connection is not established
    if(ser is None):
        print "Can't connect to the serial port"
        return

    #animation loop runs indefinitely until
    #program is forcefully terminate
    #we probably need a better way

    while True:
        try:
            #Read the data broadcasted by the arduino board
            #We're reading 7 different sensors
            line = ser.readline()
            #store it in an array
            data = [int(val) for val in line.split()]
            # test data 
            #data = [random()*1024, random()*1024,0,0,True,True,False]

            # data will now be in the follwing format
            # data[0] Channel 1 from analog pin. range: 0-1203
            # data[1] Channel 2 from analog pin. range: 0-1203
            # data[2] vertical control from analog pin. range: 0-1203 
            # data[3] horizontal control from analog pin. range: 0-1203
            # data[4] channel 1 state form digital pin. states: HIGH or LOW
            # data[5] channel 2 state form digital pin. states: HIGH or LOW
            # data[6] trigger state form digital pin. states: HIGH or LOW

            if(len(data) == 7):
                # convert voltage data from serial to appropriate voltage
                data[0], data[1] = data[0]/1023.0*10 -5 , data[1]/1023.0*10-5
                #call add data from channels with their state
                channelData.add(data[0:2],data[4:6])
                #call zoom_Handle with the zoomdata
                channelPlot.zoom_Handle(data[2:4])
                #call update with the trigger state
                channelPlot.update(channelData,data[6])
        except KeyboardInterrupt:
            plt.close()
            print "Closing ..."
            break
        except ValueError:
            pass
    ser.flush() 
    ser.close() #close the port
main()
