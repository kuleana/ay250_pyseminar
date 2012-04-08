# Katherine de Kleer
# January 23, 2012
# Homework #0

import random

class bear:
    """ define bear class according to lifespan and procreation rules """
    bear_names = []
    bear_number = 0
    pop_age = 0
    genders = ['male','female']
    bears = {'alive':{'female':[],'male':[]},'dead':{'female':[],'male':[]}}
    def __init__(self,parents,name=None,gender=None,pmale=0.5):
        """ initialize bear: name, gender, parents """
        if (gender == None):
            num = random.uniform(0,1)
            if num <= pmale:
                gender='male'
            else:
                gender='female'
        self.gender = gender
        if name == None:
            if self.gender == 'female':
                while (name in bear.bear_names or name == None):
                    name = fnames[random.randint(0,len(fnames)-1)]+' '+fnames[random.randint(0,len(fnames)-1)]
            if self.gender == 'male':
                while (name in bear.bear_names or name == None):
                    name = mnames[random.randint(0,len(mnames)-1)]+' '+mnames[random.randint(0,len(mnames)-1)]
        self.name = name
        bear.bear_names.append(self.name)
        self.age = 0
        self.lifespan = random.gauss(35,5)
        self.parents = parents
        bear.bear_number += 1
        self.alive = 1
        self.lastbirth = 0
        bear.bears['alive'][self.gender].append(self)
    def addyear(self):
        """ age bear by one year """
        self.age += 1
        self.lastbirth +=1
        if (self.age >= self.lifespan and self.alive == 1):
            self.alive = 0
            bear.bears['alive'][self.gender].remove(self)
            bear.bears['dead'][self.gender].append(self)
    def canprocreate(self):
        """ checks if a bear can mate: returns true only if a bear is female, liave, and is more than 5 years from birth or from previous birthing """
        goforit = False
        if self.gender == 'female':
            if (self.lastbirth >= 5 and self.alive):
                goforit = True  
        return goforit
    def canmate(self,mate):
        """ checks if two bears can mate: returns true if their ages, parents, livelihoods, and genders are suitable for procreation """
        goforit = False
        if self.gender != mate.gender:
            if (self.parents != mate.parents or self.parents==[] or mate.parents==[]):
                if ((self.age >= 5 and self.alive) and (mate.age >= 5 and mate.alive) and (abs(self.age-mate.age) <= 10)):
                    goforit = True
        return goforit
    def __add__(self,mate):
        """ returns a new bear with the input bears as parents """
        if self.canmate(mate):
            cub = bear([self,mate])
            self.lastbirth = 0
            mate.lastbirth = 0
            return cub
        else:
            raise Exception("That is not a suitable match for procreation!")

        
