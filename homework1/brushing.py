# brushing.py 
# homework 1c AY 250
# Feb 4, 2012
# Katherine de Kleer

""" brushing: creates interactive figure that compares different data attributes on different plots. Allows user to draw a rectangle to select a region in one plot, and subsequently highlights the corresponding datapoints in all plots. Pressing 'd' over the selected region will reset all plots """

# import packages

from pylab import *
import numpy as np
import random
import matplotlib.patches

# read in some data

data=np.loadtxt('sampledata.txt')

# initializize figure and four axes

fig=figure()
ax=fig.add_subplot(221)
ax2=fig.add_subplot(222)
ax3=fig.add_subplot(223)
ax4=fig.add_subplot(224)

npoints = len(data[:,0])
nplots = 4
pdata = zeros((npoints,nplots,2))

# control which variables get plotted against each other

pdata[:,0,0]=data[:,0]
pdata[:,0,1]=data[:,3]
pdata[:,1,0]=data[:,2]
pdata[:,1,1]=data[:,4]
pdata[:,2,0]=data[:,1]
pdata[:,2,1]=data[:,2]
pdata[:,3,0]=data[:,3]
pdata[:,3,1]=data[:,4]

# create the plots

ax.plot(pdata[:,0,0],pdata[:,0,1],'o')
ax2.plot(pdata[:,1,0],pdata[:,1,1],'o')
ax3.plot(pdata[:,2,0],pdata[:,2,1],'o')
ax4.plot(pdata[:,3,0],pdata[:,3,1],'o')

theaxes = [ax,ax2,ax3,ax4] # list of the four axes


class ClickBrowser:
    """ Class ClickBrowser: Create instances for data brushing. Use mpl_connect to send events to its functions: press, release to draw rectangle around points of interest to highlight; press 'd' over brushed region to reset all plots """
    def __init__(self):
       """ initialize a ClickBrowser instance """
       self.bottomleft = (0,0) # corners of rectangle
       self.currentind = [] # the indices for current brushed points
       self.currentaxis = ax # axis of current brushing rectangle
    def press(self,event):
       """ press: function of class Clickbrowser: accepts mouse press events from mpl_connect and stores position data in self.bottomleft """
       x = event.xdata
       y = event.ydata
       self.bottomleft = (x,y)
    def release(self,event):
       """ release: function of class ClickBrowser: accepts mouse release events from mpl_connect and combines this with the data from "press" to determine a user-described rectangle and highlight the data points inside that rectangle on all plots  """ 
       x2 = event.xdata
       y2 = event.ydata
       x1 = self.bottomleft[0]
       y1 = self.bottomleft[1]
       axis = event.inaxes
       self.currentaxis = axis
       for i in range(nplots):
            if (axis == theaxes[i]):
                axind = i
       r = matplotlib.patches.Rectangle((x1,y1),x2-x1,y2-y1,ec='blue',fc='yellow')
       axis.add_patch(r)
       ind=[]
       for i in range(npoints):
            if ((pdata[i,axind,0] <= x2) and (pdata[i,axind,0] >= x1) and (pdata[i,axind,1] <= y2) and (pdata[i,axind,1] >= y1)):
                ind.append(i)
       self.currentind = ind
       for i in range(nplots):
            theaxes[i].cla()
            theaxes[i].plot(pdata[:,i,0],pdata[:,i,1],'bo',alpha=0.2)
            theaxes[i].plot(pdata[ind,i,0],pdata[ind,i,1],'ro')
       fig.canvas.draw()
    def exitbrushing(self,event):
       """ exitbrushing: function of class ClickBrowser: accepts key events from mpl_connect and resets all plots of user presses 'd' over brushed region """ 
       axis = event.inaxes
       for i in range(nplots):
           if (axis == theaxes[i]):
               axind = i
       if ((axis == self.currentaxis) and (event.key == 'd') and (event.xdata <= max(pdata[self.currentind,axind,0])) and (event.xdata >= min(pdata[self.currentind,axind,0])) and (event.ydata <= max(pdata[self.currentind,axind,1])) and (event.ydata >= min(pdata[self.currentind,axind,1]))): 
            for i in range(nplots):
                theaxes[i].cla()
                theaxes[i].plot(pdata[:,i,0],pdata[:,i,1],'bo')
       fig.canvas.draw()

clicker = ClickBrowser() # create an instance of ClickBrowser class

# define mpl_connect interactions
fig.canvas.mpl_connect('button_press_event',clicker.press)
fig.canvas.mpl_connect('button_release_event',clicker.release)
fig.canvas.mpl_connect('key_press_event',clicker.exitbrushing)

show()

