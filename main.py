import serial  # python's serial communication package
import numpy as np  # numerical processing package
from collections import deque  # data structure to store serial data
import matplotlib.pyplot as plt  # 2D graphing package
from random import random  # random signal generator for testing
from scipy.signal import butter, filtfilt  # signal processors
from math import sin
from threading import Thread
# handles data from the channels


class ChannelData:

    def __init__(self, maxLen):
    	self.maxLen = maxLen
    	self.reset(1)  # reset both channels
    	self.reset(2)

    def reset(self, channel):
        if(channel == 1):
        	self.channel1 = deque([0.0] * self.maxLen)
        if(channel == 2):
            self.channel2 = deque([0.0] * self.maxLen)

    def addToBuf(self, buf, val):
       # if(len(buf) < self.maxLen):
        #    buf.append(val)
        #else:
        buf.pop()
        buf.appendleft(val)

    def add(self, data, toggle):
    	if(toggle[0]):  # if the first channel is on
    	    self.addToBuf(self.channel1, data[0])
    	else:
    		self.reset(1)
    	if(toggle[1]):
    		self.addToBuf(self.channel2, data[1])
    	else:
    		self.reset(2)

# handles plotting


class ChannelPlot:
	ylim = [-5,5]
	xlim = [0,100]
	div = 2
	current = 1
	data = [1,2,4,8]

	def __init__(self, ChannelData):

		plt.ion()
		self.ch1, = plt.plot(ChannelData.channel1)  # data curve for channel 1
		self.ch2, = plt.plot(ChannelData.channel2)  # data curve for channel 2
		# This should be handled by a zooming method
		plt.ylim(self.ylim)
		plt.xlim(self.xlim)
		#
		plt.grid()  # enable oscilloscope grid like look
		plt.gca().axes.xaxis.set_ticklabels([])  # disable axes labels
		plt.gca().axes.yaxis.set_ticklabels([])
		plt.gcf().canvas.set_window_title('Oscilloscope')  # title
		
		# Handle by zoom method
		plt.ylabel(str(self.div)+"V per divison")
		plt.xlabel("1s per division")
		plt.draw()
		#

	def update(self, ChannelData, trigger):
		if(trigger):  # don't update if trigger is enabled
		    return
		self.ch1.set_ydata(ChannelData.channel1)
		self.ch2.set_ydata(ChannelData.channel2)
		plt.draw()

	def zoom_Handle(self,level):
		ver = level[0]
		hor = level[1]
		divider = self.data[ver/256]
		if(divider == self.current):
			return
		self.current = divider
		self.div = 2.0/divider
		self.ylim[0] = -5.0/divider
		self.ylim[1] = 5.0/divider
		plt.ylabel(str(self.div)+"V per divison")
		plt.xlabel("1s per division")
		plt.ylim(self.ylim)
		#plt.xlim(xlim)

class ForThread:
	def __init__(self,channelData,channelPlot,communicator,serial):
		self.channelData = channelData
		self.channelPlot = channelPlot
		self.proceed = communicator
		self.ser = serial
	def __call__(self):
		i = 0
		init = 0
		#lock=Lock()
		while self.proceed[0]:
		    line = self.ser.readline()
		    data = [int(val) for val in line.split()]
		    if(len(data)==7):
		    	data[0], data[1] = data[0]/1023.0*10 -5 , data[1]/1023.0*10-5
		       	self.channelData.add(data[0:2],data[4:6])
		    	self.channelPlot.zoom_Handle(data[2:4])
				#self.channelData.extBuf.appendleft(data[0])
			
def main():
	strPorts = ['/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyACM2', '/dev/ttyACM3']
	channelData = ChannelData(100)
	channelPlot = ChannelPlot(channelData)

	for strPort in strPorts:
	    try:
	        ser = serial.Serial(strPort, 9600)
	    except Exception:
	        pass

    # animation loop
	while True:
		try:
        # the commented lines only work if there is a serial connection
		    line = ser.readline()
		    data = [int(val) for val in line.split()]
		    # test Data
		    #data = [random()*10-5, random()*10-5,random(),random(),True,False,False]
		    if(len(data) == 7):
		    	# convert voltage data from serial to appropriate voltage
		    	data[0], data[1] = data[0]/1023.0*10 -5 , data[1]/1023.0*10-5
		    	channelData.add(data[0:2],data[4:6])
		    	channelPlot.zoom_Handle(data[2:4])
		    	channelPlot.update(channelData,data[6])
		except KeyboardInterrupt:
		    plt.close()
		    print "Closing ..."
		    break
		except ValueError:
			pass
	ser.flush()
	ser.close()
main()