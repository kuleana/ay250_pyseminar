# paperplot.py - reproduce paper figure
# Homework 1a AY 250
# Feb 4, 2012
# Katherine de Kleer

""" paperplot: produces a plot with images of Uranus with three different filters, including colorbars """

# import packages
from pylab import *
from matplotlib import cm
import Image
from matplotlib import colorbar
import matplotlib.pyplot as plt

# read in data from file
dataH = plt.imread('uranusH.jpg')
dataJ = plt.imread('uranusJ.jpg')
dataK = plt.imread('uranusK.jpg')
dataH = dataH.sum(2)
dataJ = dataJ.sum(2)
dataK = dataK.sum(2)

# create plots of data, resizing to center image
f,(axJ,axH,axK)=subplots(1,3)
f.set_figwidth(15)
H=axH.imshow(dataH[60:510,20:500],cmap=cm.Greys_r)
J=axJ.imshow(dataJ[50:520,200:700],cmap=cm.Greys_r)
K=axK.imshow(dataK[50:520,30:530],cmap=cm.Greys_r)

# get rid of all ticks on plots
axH.xaxis.set_ticks([])
axH.yaxis.set_ticks([])
axJ.xaxis.set_ticks([])
axJ.yaxis.set_ticks([])
axK.xaxis.set_ticks([])
axK.yaxis.set_ticks([])

# create wavelength annotations
axH.text(10, 35, r'1.63$\mu$m', fontsize=12, color='white',weight='bold')
axJ.text(10, 35, r'1.25$\mu$m', fontsize=12, color='white',weight='bold')
axK.text(10, 35, r'2.20$\mu$m', fontsize=12, color='white',weight='bold')

# create & customize colorbars for each plot
kwH={'orientation':'vertical','fraction':0.04,'anchor':(0,.5),'pad':0}
axHbar, kwH = colorbar.make_axes(axH,**kwH)
cbH = colorbar.Colorbar(axHbar, H)
cbH.set_label('counts')
cbH.set_ticks(linspace(0,300,4))

kwJ={'orientation':'vertical','fraction':0.04,'anchor':(0,0.5),'pad':0}
axJbar, kwJ = colorbar.make_axes(axJ,**kwJ)
cbJ = colorbar.Colorbar(axJbar, J)
cbJ.set_label('counts')
cbJ.set_ticks(linspace(0,507,4))

kwK={'orientation':'vertical','fraction':0.04,'anchor':(0,0.5),'pad':0}
axKbar, kwK = colorbar.make_axes(axK,**kwK)
cbK = colorbar.Colorbar(axKbar, K)
cbK.set_label('counts')
cbK.set_ticks(linspace(0,750,4))

show()
