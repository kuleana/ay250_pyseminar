# Katherine de Kleer
# March 4, 2012 - homework for AY250
""" client.py: reads in images, sends them through various image manipulation methods on a remote server, then reverses these methods to recover original image. Saves a file containing rows with the original image, manipulated image, and recovered image for each method. Output file is in png format and is named 'input_filename_result.png' """

# Import Packages
import matplotlib.pyplot as plt
import numpy as np
import xmlrpclib, sys
from skimage import color
from matplotlib.pyplot import subplots

# Input server information
host, port = "50.0.142.70", 5021
server = xmlrpclib.ServerProxy("http://%s:%d" % (host, port))

# Read in files (path & files hard-coded)
path = 'photos/'
files = ['bugs.jpg','temple.jpg','magnets.jpg']

images = []
first=True
for item in files:
    data = np.flipud(plt.imread(path+item))
    if first:
        # convert one image to grayscale to test server capabilities
        data = color.rgb2gray(data)
        data = np.array([x*255 for x in data],dtype=np.uint8)
        first = False
    images.append(data)

for i in range(len(images)):
    image = images[i]
    
    # Invert method
    inverted = np.array(server.invert(image.tolist()),dtype=np.uint8)
    uninverted = [255-x for x in inverted]
    # Rotate method
    rotated = np.array(server.rotate180(image.tolist()),dtype=np.uint8)
    unrotated = np.flipud(np.fliplr(rotated))
    # Shift Hue method
    shifted = np.array(server.shiftHue(image.tolist()),dtype=np.uint8)
    hsvshifted = color.rgb2hsv([x/255. for x in np.array(shifted,dtype=np.uint8)])
    hsvunshifted = hsvshifted
    hsvunshifted[:,:,0] = [np.mod(x+0.5,1) for x in hsvshifted[:,:,0]]
    unshifted = [np.uint8(x*255) for x in color.hsv2rgb(hsvunshifted)]

    if len(image.shape) == 2:
        pickcolors = plt.cm.gray
    else:
        pickcolors = plt.cm.prism

    # Create 3x3 plot demonstrating methods
    f,ax=subplots(3,3)
    ax[0,0].imshow(image,cmap=pickcolors)
    ax[0,0].set_title('Original Images')
    ax[0,0].set_ylabel('Inverted')
    ax[0,1].imshow(inverted,cmap=pickcolors)
    ax[0,1].set_title('Modified Images')
    ax[0,2].imshow(uninverted,cmap=pickcolors)
    ax[0,2].set_title('Recovered Images')
    ax[1,0].imshow(image,cmap=pickcolors)
    ax[1,0].set_ylabel('Rotated')
    ax[1,1].imshow(rotated,cmap=pickcolors)
    ax[1,2].imshow(unrotated,cmap=pickcolors)
    ax[2,0].imshow(image,cmap=pickcolors)
    ax[2,0].set_ylabel('Hue Shifted')
    ax[2,1].imshow(shifted,cmap=pickcolors)
    ax[2,2].imshow(unshifted,cmap=pickcolors)
    for row in ax:
        for axis in row:
            axis.xaxis.set_ticks([])
            axis.yaxis.set_ticks([])

    # Output to file
    a=files[i]
    outfilen = a.split('.')[0]+'_results.png'
    plt.savefig(outfilen,format='png')
    
