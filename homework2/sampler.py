# Katherine de Kleer 02/09/12
# Homework #2 AY 250

import scipy
from scipy.stats import *
import numpy as np

def sampler(ff,gg,n):

    """ function sampler(ff,gg,n): attempts to imitate the pdf of a target distribution f(x) using rejection sampling on a reference distribution g(x). Inputs: ff - f(x) in string format, gg - g(x) as a scipy.stats object, n - numer of requested samples """
 
    # Calculate best M value
    print 'SAMPLER: calculating M value'
    m = .99
    testx = np.linspace(0,10,500)
    mgood = False
    while mgood == False:
        m += 0.01
        badx = 0
        for x in testx:
            fx = eval(ff)
            gx = gg.pdf(x)
            if (fx >= m*gx):
                badx += 1
        if (badx == 0):
            mgood = True

    # Create distribution
    samples = []
    naccept = 0 # number of samples accepted
    ntotal = 0 # number of samples attempted
    while naccept < n:
        ntotal += 1
        x = gg.rvs()
        u = uniform.rvs()
        fxc = eval(ff)
        gxc = gg.pdf(x)
        if (u < fxc/(m*gxc)):
            samples.append(x)
            naccept += 1

    return m, samples, float(naccept)/float(ntotal)
