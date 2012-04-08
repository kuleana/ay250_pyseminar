# import packages, specify plugins
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as ndi
from skimage import io, filter, data, color, feature
from scipy.misc import imresize
from sklearn.ensemble import RandomForestClassifier
io.use_plugin('matplotlib')
import os
from scipy.stats import skew, variation, pearsonr
from copy import copy
from numpy import random
from sklearn import metrics,grid_search

def classifier(test='50_categories',target='validation',validate=False,quick=False):

    """classifier(test='test/',target='target/',validate=False,verbose=False): function that attempts to classify a set of images based on a set of learning images, using various image features. If validate=False, classifier uses half the testing set as a target set, and outputs statistics on its performance. If validate=True, classifier uses the entire test directory to train on, and outputs a list of the target files with predicted classification. If quick=True, classifier uses only the first 5 images in each category to train on. Note on paths: training path expects a directory with subdirectories named with the category label, and validation path expects a directory of images"""

    print '%CLASSIFIER: Reading Input Files' # status update
    test = test+'/'
    target = target+'/'

    # read in files, store data and categories
    dir=test
    subdir=os.listdir(dir)
    for element in subdir:
        if element[0]=='.':
            subdir.remove(element) # eliminate non-image  entries
    images=[] # store images
    categories=[] # store name of categories for each image
    catint=[] # store integer designation of category for each image
    filens=[] # store names of files
    i=-1
    for cat in subdir: # loop over directories
        i+=1
        files=os.listdir(dir+cat)
        if quick==True: # speed-learning: 5 images per category
            files=files[:4]
        for element in files:
            if element[0]=='.':
                files.remove(element) # eliminate non-image entries
        categories.append(cat)
        for item in files: # look over files
            catint.append(i)
            images.append(np.flipud(plt.imread(dir+cat+'/'+item)))
            filens.append(item)

    # repeat for testing set, if different from target set
    if validate == True:
        valdir=target
        valimages=[]
        valfilens = os.listdir(valdir)
        for item in valfilens:
            if item[0]=='.':
                valfilens.remove(item)
        for item in valfilens:
            valimages.append(np.flipud(plt.imread(valdir+item)))

    # names of features for class Featured
    featnames=['Total Number of Pixels','Aspect Ratio','Median Number of Edges',\
                'Fraction of Color in Red','Fraction of Color in Green',\
                'Fraction of Color in Green','Fraction of Edges in Vertical Orientation',\
                'Skewness in Red Channel','Variation in Blue Channel','Brightness Centering',\
                'Correlation Between Red and Blue Channels',\
                'Correlation Between Red and Green Channels',\
                'Correlation Between Blue and Green Channels','Number of Connected Bright Objects',\
                'Number of Connected Dim Objects']

    nim = len(catint) # number of images
    nfeat = len(featnames) # number of features
    features = np.zeros((nim,nfeat)) # store feature values for each image
    statuspoints = np.linspace(0,nim,11) # for status update calculations
    statuspoints = [np.floor(pt) for pt in statuspoints]
    if validate == True:
        nval = len(valfilens) # number of validation images
        valfeatures = np.zeros((nval,nfeat)) # store feature values for validation images

    # calculate features for images in training set
    print '%CLASSIFIER: Calculating Features' # status update
    statusn = 0
    for i in range(nim):
        # STATUS UPDATE
        if i in statuspoints:
            # print status update about every 10% complete
            print '%CLASSIFIER: '+theraven(statusn)+' ['+str(i*100/nim)+'%]'
            statusn+=1
        im = Featured(images[i])
        features[i,0]=im.ncountpix()
        features[i,1]=im.aspect()
        features[i,2]=im.mededges()
        features[i,3]=im.redfrac()
        features[i,4]=im.greenfrac()
        features[i,5]=im.bluefrac()
        features[i,6]=im.vedges()
        features[i,7]=im.redskew()
        features[i,8]=im.bluevar()
        features[i,9]=im.centered()
        features[i,10]=im.rgcor()
        features[i,11]=im.rbcor()
        features[i,12]=im.bgcor()
        features[i,13]=im.nbright()
        features[i,14]=im.ndim()

    # calculate features for images in validation set
    if validate == True:
        print '%CLASSIFIER: Calculating Validation Set Features'
        for i in range(nval):
            im = Featured(valimages[i])
            valfeatures[i,0]=im.ncountpix()
            valfeatures[i,1]=im.aspect()
            valfeatures[i,2]=im.mededges()
            valfeatures[i,3]=im.redfrac()
            valfeatures[i,4]=im.greenfrac()
            valfeatures[i,5]=im.bluefrac()
            valfeatures[i,6]=im.vedges()
            valfeatures[i,7]=im.redskew()
            valfeatures[i,8]=im.bluevar()
            valfeatures[i,9]=im.centered()
            valfeatures[i,10]=im.rgcor()
            valfeatures[i,11]=im.rbcor()
            valfeatures[i,12]=im.bgcor()
            valfeatures[i,13]=im.nbright()
            valfeatures[i,14]=im.ndim()

    # building testing and target sets
    if validate==False:
        testim = images[::2]
        targim = images[1::2]
        testfeat = features[::2,:]
        targfeat = features[1::2,:]
        targfiles = filens[1::2]
        testcat = catint[::2]
        targcat = catint[1::2]
    else:
        testim = images
        targim = valimages
        testfeat = features
        targfeat = valfeatures
        targfiles = valfilens
        testcat = catint

    # build random forest 
    print '%CLASSIFIER: Building Random Forest' # status update
    rfc = RandomForestClassifier(compute_importances=True)
    rfc = rfc.fit(testfeat,testcat)
    impt = rfc.feature_importances_
    pred = rfc.predict(targfeat) # predicted categories for target images
    ncat=max(catint)

    if validate == False:
        randpred = [] # predictions for targcat based on random guessing
        for i in range(len(targim)):
            randpred.append(random.randint(0,ncat+1))
        score = metrics.zero_one_score(targcat, pred) # zero-one score
        randscore = metrics.zero_one_score(targcat, randpred) # zero-one score for random guessing
        # outputs
        print 'Three Most Important Features:'
        for ifeat in range(3):
            maxind = np.where(impt == np.max(impt))
            impt[maxind[0]]=0
            print str(ifeat+1)+'. '+featnames[maxind[0]]

        print str(int(score*100))+'% Good Predictions from Random Forest'
        print str(int(randscore*100))+'% Good Predictions from Random Guessing'
    else:
        print 'filename\t\tpredicted_class'
        print '-'*50
        for i in range(len(targfiles)):
            name = targfiles[i]+' '*(30-len(targfiles[i]))
            print name+'\t'+categories[pred[i]]

class Featured:
    """ Featured(image): takes gray or RGB images as input, contains numerous methods that return a single float parameterization of a specific characteristic of the image. """
    def __init__(self,im):
        self.fullsize = im # original image
        self.shape = im.shape
        if len(im.shape)==3: # distinguish between gray & RGB images
            self.threed=True
        else:
            self.threed=False
        size = max(im.shape[0],im.shape[1])
        if size >= 500: # if images are too big, resize them
            scale = np.ceil(size/500.)
            im =imresize(im,(int(im.shape[0]/scale),int(im.shape[1]/scale)))
        self.image = im # resized image
        if self.threed==True:
            self.gray = color.rgb2gray(im)
            self.red = im[:,:,0]
            self.green = im[:,:,1]
            self.blue = im[:,:,2]
        else:
            self.gray = im
    # define features
    def ncountpix(self):
        """n=ncountpix(): returns float number of pixels in an RGB image"""
        np=self.shape[0]*self.shape[1]
        return float(np)
    def aspect(self):
        """x=aspect(): returns aspect ratio of an RGB image"""
        asp=float(self.shape[0])/float(self.shape[1])
        return asp
    def mededges(self):
        """x=mededges(): returns a parameterization of the number of edges in an RGB image"""
        edges=filter.sobel(self.gray)
        med=np.median(edges)
        return med
    def redfrac(self):
        """x=redfrac(): returns the fraction of color in the red channel in an RGB image"""
        if self.threed==True:
            s1=self.image[:,:,0].sum()
            s2=self.image.sum()
            return float(s1)/float(s2)
        else:
            return float(0)
    def greenfrac(self):
        """x=greenfrac(): returns the fraction of color in the green channel in an RGB image"""
        if self.threed==True:
            s1=self.image[:,:,1].sum()
            s2=self.image.sum()
            return float(s1)/float(s2)
        else:
            return float(0)
    def bluefrac(self):
        """x=bluefrac(): returns the fraction of color in the blue channel in an RGB image"""
        if self.threed==True:
            s1=self.image[:,:,2].sum()
            s2=self.image.sum()
            return float(s1)/float(s2)
        else:
            return float(0)
    def vedges(self):
        """x=vedges(): returns a parameterization of the number of vertical edges versus total edges in an RGB image"""
        hprew=filter.hprewitt(self.gray)
        vprew=filter.vprewitt(self.gray)
        vfrac=vprew.sum()/(vprew.sum()+hprew.sum())
        return vfrac
    def redskew(self):
        """x=redskew(): returns the skew of brightness within the red channel in an RGB image"""
        if self.threed==True:
            red=self.image[:,:,0]
            flat = [x for sublist in red for x in sublist]
            redskew=skew(flat)
            return redskew
        else:
            return float(0)
    def bluevar(self):
        """x=bluevar(): returns the variation in brightness within the blue channel of an RGB image"""
        if self.threed==True:
            blue=self.image[:,:,2]
            flat = [x for sublist in blue for x in sublist]
            bluevar=variation(flat)
            return bluevar
        else:
            return float(0)
    def centered(self):
        """x=centered(): returns the fraction of brightness within the middle 50% of an RGB image"""
        nx=len(self.gray[:,0])
        ny=len(self.gray[0,:])
        mid=self.gray[nx/4.:3.*nx/4.,ny/4.:3.*ny/4.]
        midfrac=mid.sum()/self.gray.sum()
        return midfrac
    def rbcor(self):
        """x=rbcor(): returns the correlation between red and blue channels in an RGB image"""
        if self.threed==True:
            red=self.image[:,:,0]
            blue=self.image[:,:,2]
            rflat = [x for sublist in red for x in sublist]
            bflat = [x for sublist in blue for x in sublist]
            p = pearsonr(rflat,bflat)
            return p[0]
        else:
            return float(0)
    def rgcor(self):
        """x=rgcor(): returns the correlation between red and green channels in an RGB image"""
        if self.threed==True:
            rflat = [x for sublist in self.red for x in sublist]
            gflat = [x for sublist in self.green for x in sublist]
            p = pearsonr(rflat,gflat)
            return p[0]
        else:
            return float(0)
    def bgcor(self):
        """x=bgcor(): returns the correlation between blue and green channels in an RGB image"""
        if self.threed==True:
            bflat = [x for sublist in self.blue for x in sublist]
            gflat = [x for sublist in self.green for x in sublist]
            p = pearsonr(bflat,gflat)
            return p[0]
        else:
            return float(0)
    def nbright(self):
        """x=nbright(): returns the number of connected units in the top 1/8 of brightness within an RGB image"""
        flat = [x for sublist in self.gray for x in sublist]
        flatcp = copy(flat)
        nx = len(flatcp)
        flatcp.sort()
        cutoff = flatcp[int(nx*7./8.)]
        bright = (flat >= cutoff)
        labels,count=ndi.label(bright)
        return float(count)
    def ndim(self):
        """x=ndim(): returns the number of connected units in the bottom 1/8 of brightness within an RGB image"""
        flat = [x for sublist in self.gray for x in sublist]
        flatcp = copy(flat)
        nx = len(flatcp)
        flatcp.sort()
        cutoff = flatcp[int(nx*1./8.)]
        bright = (flat >= cutoff)
        labels,count=ndi.label(bright)
        return float(count)

def theraven(n):
    """ theraven(n): returns the nth line of Edgar Allen Poe's 'The Raven' for n<20 """
    poem=['once upon a midnight dreary','while I pondered weak and weary','over many a quaint and curious','volume of forgotten lore','while I nodded, nearly napping','suddenly there came a tapping','as of someone gently rapping,','rapping at my chamber door','tis some visitor, I muttered','tapping at my chamber door','only this, and nothing more.','Ah distinctly I remember','it was in the bleak December','and each separate dying ember','wrought its ghost upon the floor','eagerly I wished the morrow;','vainly I had sought to borrow','from my books surcease of sorrow','sorrow for the lost Lenore','for the rare and radiant maiden','whom the angels named Lenore','nameless here forevermore']
    return poem[n]

