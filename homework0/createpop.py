# Katherine de Kleer
# January 23, 2012
# Homework #0

import time
import random
import copy
from getnames import getnames
fnames, mnames = getnames() # create & retrieve name lists

def createpop(nyears,pmale=0.5):
    """createpop(nyears,pmale=0.5): Creates a population of bears over nyears with probability of a male birth pmale. Returns the bear population in dictionary format with keys 'alive' and 'dead' and subkeys for each of 'male' and 'female' """
    
    # import and re-initialize every run
    import bear 
    reload(bear)
    from bear import bear

    # INITIALIZE BEAR POPULATION

    a = bear([],name='MARY',gender='female')
    b = bear([],name='ADAM',gender='male')
    c = bear([],name='EVE',gender='female')

    tstart=time.time()

    # GROW BEAR POPULATION

    for year in range(nyears):
        tt = time.time()
        bear.pop_age += 1
        for boybear in bear.bears['alive']['male']: boybear.addyear()
        potentialmoms = copy.copy(bear.bears['alive']['female'])
        for girlbear in potentialmoms:
            girlbear.addyear()
            if girlbear.canprocreate():
                mated = False
                potentialmates = copy.copy(bear.bears['alive']['male'])
                random.shuffle(potentialmates)
                i = -1
                # loop through living male bears until a mate is found
                # then spawn new bear
                while (i+1 < len(potentialmates) and mated == False):
                    i += 1
                    if girlbear.canmate(potentialmates[i]):
                        newbear = girlbear + potentialmates[i]
                        mated = True

#    tend=time.time()
#    print 'Total time of run: ',int(tend-tstart),' seconds'

    return bear.bears




