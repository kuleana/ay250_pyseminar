# homework1b.py - creates imitation plot of given data
# homework 1b AY 250
# Feb 4, 2012
# Katherine de Kleer

# import packages
import numpy as np
from pylab import *

# read in the data from file
kw={'skiprows':1}
nytemps = np.loadtxt('ny_temps.txt',**kw) #MJD, max temp
google = np.loadtxt('google_data.txt',**kw) #MJD, stock value
yahoo = np.loadtxt('yahoo_data.txt',**kw)

# initialize figure
f=figure()
f.set_figwidth(10)
f.set_figheight(8)

# plot stocks
plt.plot(yahoo[:,0],yahoo[:,1],color='purple',linewidth=2,label='Yahoo! Stock Value')
plt.plot(google[:,0],google[:,1],color='blue',linewidth=2,label='Google Stock Value')
ax=plt.gca()
titlekw={'weight':'bold','size':26,'fontname':'Times New Roman'}
ax.set_title('New York Temperature, Google, and Yahoo!',**titlekw)
ax.set_xlim((48800,55600))
ax.set_ylim((-10,770))
fontkw={'size':14}
ax.set_ylabel('Value (Dollars)',**fontkw)
ax.set_xlabel('Date (MJD)',**fontkw)

# plot temperatures
ax2=ax.twinx()
ax2.plot(nytemps[:,0],nytemps[:,1],color='red',linestyle='--',linewidth=2,label='NY Mon. High Temp')
ax2.set_ylabel(r'Temperature ($^o$F)',**fontkw)
ax2.set_ylim((-150,100))
ax2.set_xlim((48800,55600))

# create & position legend
l=ax.legend(loc=(0.01,0.45))
l.draw_frame(False)
l2=ax2.legend(loc=(0.01,0.4))
l2.draw_frame(False)

show()
