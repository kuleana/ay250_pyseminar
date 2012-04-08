# Katherine de Kleer 02/09/2012
# Homework #2 for AY 250

import sampler
from sampler import sampler
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import math

def getdist(question):

    """ function getdist(question): calls function sampler with various parameters, then outputs plots and prints acceptance rates and other values of interest. Accepts inputs 'b' 'c' or 'd' """

    if question == 'b':

        # PART B

        # Define inputs
        ff = '(1.0/2.0)*np.exp(-abs(x))' # Laplace(0,1)
        gg = stats.cauchy
        n = 1000

        # Call sampler
        m, samples, ratio = sampler(ff,gg,n)

        # Create distributions and perform K-S test
        grid = np.linspace(-10,10,num=1000)
        actual = []
        cc = []
        for x in grid:
            actual.append(eval(ff))
            cc.append(stats.cauchy.pdf(x))
            ks = stats.kstest(samples,'laplace')

        # Print and plot relevant information
        print 'calculated M value: ',m
        print 'acceptance rate: ',int(ratio*100),'%'
        print 'K-S test finds a ',int(ks[1]*100),'% chance that these points were sampled from a Laplace(0,1) distribution'

        plt.hist(samples,50,normed=True,label='samples')
        plt.plot(grid,actual,linewidth=3,color='red',linestyle='--',label='f(x)')
        plt.plot(grid,[m*cci for cci in cc],color='green',label='Mg(x)')
        plt.title('Histogram of Samples, with Laplace(0,1) Distribution')
        plt.legend()

        plt.show()

    if question == 'c':

        # PART C

        # Define inputs
        ff = '(1.0/2.0)*np.exp(-abs(x))'
        gg = stats.t(2)
        n = 1000

        # Call sampler
        m, samples, ratio = sampler(ff,gg,n)
        mb, samplesb, ratiob = sampler(ff,stats.cauchy,n)

        # Create distributions
        grid = np.linspace(-10,10,num=1000)
        actual=[]
        st=[]
        for x in grid:
            actual.append(eval(ff))
            st.append(stats.t.pdf(x,2))

        # Print and plot relevant information
        print 'calculated M value: ',m
        print 'acceptance rate: ',int(ratio*100),'%'
        print 'compare to acceptance rate of ',int(ratiob*100),'% from part b'

        plt.hist(samples,50,normed=True,label='samples')
        plt.plot(grid,actual,linewidth=3,color='red',linestyle='--',label='f(x)')
        plt.plot(grid,[m*sti for sti in st],color='green',label='Mg(x)')
        plt.title('Histogram of Samples, with Laplace(0,1) Distribution')
        plt.legend()

        plt.show()

    if question == 'd':

        # PART D

        # Define inputs
        ff = 'np.sqrt(2/np.pi)*x**2*np.exp(-x**2/2)'
        gg = stats.truncnorm(-math.pi/2,10,loc=math.pi/2)
        n = 5000

        # Call sampler
        m, samples, ratio = sampler(ff,gg,n)

        # Create distributions
        grid = np.linspace(0,10,num=1000)
        actual=[]
        nm=[]
        for x in np.linspace(0,10,num=1000):
            actual.append(eval(ff))
            nm.append(stats.truncnorm.pdf(x,-math.pi/2,10,loc=math.pi/2))
            ks = stats.kstest(samples,'maxwell')

        # Print and plot relevant information
        print 'calculated M value: ',m
        print 'acceptance rate: ',int(ratio*100),'%'
        print 'K-S test finds a ',int(ks[1]*100),'% chance that these points were sampled from a Maxwell distribution'

        plt.hist(samples,50,normed=True,label='samples')
        plt.plot(grid,[m*nmi for nmi in nm],color='blue',label='Mg(x)')
        plt.plot(grid,actual,linewidth=3,color='red',linestyle='--',label='f(x)')
        plt.title('Histogram of Samples, with Maxwell Distribution')
        plt.legend()

        plt.show()


