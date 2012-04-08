# Katherine de Kleer
# 3/16/12
# AY 250 homework #6
# imagesearch.py: creates GUI that allows user to type in search keywords through an image search via Google. GUI displays image, image URL, and allows user to perform a few image manipulations.

import matplotlib
from skimage.morphology import skeletonize
from skimage.color import rgb2hsv, hsv2rgb
from scipy.misc import imresize
matplotlib.use('WXAgg')
from enthought.traits.api import *
from enthought.traits.ui.api import View, Item, ButtonEditor, Group, HSplit, HGroup, VGroup
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
import wx
import urllib
import urllib2
import json
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from enthought.traits.ui.wx.editor import Editor
from enthought.traits.ui.wx.basic_editor_factory import BasicEditorFactory

# build url opener to circumvent certain permission issues
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

class _MPLFigureEditor(Editor):

    scrollable  = True

    def init(self, parent):
        self.control = self._create_canvas(parent)
        self.set_tooltip()

    def update_editor(self):
        pass

    def _create_canvas(self, parent):
        # The panel lets us add additional controls.
        panel = wx.Panel(parent, -1, style=wx.CLIP_CHILDREN)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        # matplotlib commands to create a canvas
        mpl_control = FigureCanvas(panel, -1, self.value)
        sizer.Add(mpl_control, 1, wx.LEFT | wx.TOP | wx.GROW)
        toolbar = NavigationToolbar2Wx(mpl_control)
        sizer.Add(toolbar, 0, wx.EXPAND)
        self.value.canvas.SetMinSize((20,20))
        return panel

class MPLFigureEditor(BasicEditorFactory):

    klass = _MPLFigureEditor

class ImageDisplay(HasTraits):
        "ImageDisplay(HasTraits): Creates a Traits UI image display for a Google image search. Allows user input of search keywords, displays the image URL and image itself, and allows for image manipulation """

        figure = Instance(Figure, ())
        search_terms = Str('Enter search keywords')
        rotate = Button()
        rotate_Scale = Button()
        rotate_Hue = Button()
        run_query = Button()
        image_url = Str('none')

        def __init__(self):
            super(ImageDisplay, self).__init__()
            axes = self.figure.add_subplot(111)
            self.ax = axes
            image = np.flipud(plt.imread('default.jpg'))
            self.image = image
            axes.imshow(image)

        def _rotate_fired(self):
            """" _rotate_fired(self): rotates and re-displays image when button is pressed """
            newimage = np.rot90(self.image)
            self.image = newimage
            self.ax.imshow(newimage)
            self.figure.canvas.draw()

        def _rotate_Hue_fired(self):
            """" _rotate_Hue_fired(self): rotates hue and re-displays image when button is pressed """
            max = 255. 
            hsvimage = rgb2hsv([x/max for x in self.image])
            hsvimage[:,:,0] = [np.mod(x+0.5,1) for x in hsvimage[:,:,0]]
            hsvimage = [np.uint8(x*max) for x in hsv2rgb(hsvimage)]
            self.image = hsvimage
            self.ax.imshow(hsvimage)
            self.figure.canvas.draw()

        def _rotate_Scale_fired(self):
            """" _rotate_Scale_fired(self): rotates scale and re-displays image when button is pressed """
            max = 255. # this will only work with certain image types...
            hsvimage = rgb2hsv([x/max for x in self.image])
            hsvimage[:,:,1] = [np.mod(x+0.5,1) for x in hsvimage[:,:,1]]
            hsvimage = [np.uint8(x*max) for x in hsv2rgb(hsvimage)]
            self.image = hsvimage
            self.ax.imshow(hsvimage)
            self.figure.canvas.draw()

        def _run_query_fired(self):
            """" _run_query_fired(self): runs a new image search on the contents of the input box, and displays image & url """
            search = self.search_terms
            search = urllib.quote(search) # url formatting
            searchurl = ('https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q='+search+'&as_filetype=jpg')
            response = opener.open(searchurl)
            results = json.load(response)
            nres = len(results['responseData']['results']) # number of results
            picpage='none'
            for i in range(nres):
                # try reading results sequentially until an exception is not raised
                try:
                    url=results['responseData']['results'][i]['url']
                    self.image_url = url
                    picfile = urllib2.urlopen(url)
                    picpage = picfile.read()
                    break
                except: pass
            # if an exception is raised for every image available, output error message
            if picpage=='none': self.search_terms = 'No Images Available! Try Another Search.'
            else:
                output = open('temp_pic.jpg','wb')
                output.write(picpage) # write file
                output.close()
                queryimage = np.flipud(plt.imread('temp_pic.jpg'))
                size = max(queryimage.shape[0],queryimage.shape[1])
                if size >= 500: # if images are too big, resize them
                    scale = np.ceil(size/500.)
                    queryimage =imresize(queryimage,(int(queryimage.shape[0]/scale),int(queryimage.shape[1]/scale)))
                if len(queryimage.shape)==2: # if image is black&white, make into three-channel
                    threed=np.zeros(queryimage.shape[0],queryimage.shape[1],3)
                    threed[:,:,0]=queryimage
                    threed[:,:,1]=queryimage
                    threed[:,:,2]=queryimage
                    queryimage=threed
                self.image = queryimage
                self.ax.imshow(queryimage)
                self.figure.canvas.draw()

        def _search_terms_changed(self,old,new):
            """ _search_terms_changed(self,old,new): updates attribute to match contents of input box"""
            self.search_terms = str(new)

        # Specify GUI View
        view = View(VGroup(
                        HGroup(Item('search_terms',show_label=False,width=300),
                        Item('run_query',show_label=False),springy=True,columns=2,label='Input',show_border=True),
                        HGroup(Item('image_url',style='readonly'),label='url',show_border=True),
                        HGroup(Item('figure', editor=MPLFigureEditor(),
                                show_label=False,name='Image Display'),label='Image Display',show_border=True),
                        VGroup(Item('rotate',show_label=False),
                        Item('rotate_Scale',show_label=False),
                        Item('rotate_Hue',show_label=False),label='Image Manipulation Options',show_border=True)),
                        title='Google Image Search',
                        width=600,
                        height=700,
                        resizable=True)

#Counter().configure_traits()
ImageDisplay().configure_traits()
