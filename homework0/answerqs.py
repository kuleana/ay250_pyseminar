def answerqs(question):

    import createpop
    import numpy

    if question == 'aa':

        nruns = 100
        nyears = 100
        nbears = []

        for i in range(nruns):
            bears = createpop.createpop(nyears)
            nborn = len(bears['alive']['male'])+len(bears['alive']['female'])+len(bears['dead']['male'])+len(bears['dead']['female'])
            nbears.append(nborn)

        meanbirths = numpy.mean(nbears)
        stddev = numpy.std(nbears)

        print 'average births in first 100 years: ',meanbirths,' +/- ',stddev

    if question == 'ab':

        nruns = 10
        nyears = 150
        nalive = []

        for i in range(nruns):
            bears = createpop.createpop(nyears)
            alivebears = len(bears['alive']['male'])+len(bears['alive']['female'])
            nalive.append(alivebars)

        meanliving = numpy.mean(nalive)
        stddev = numpy.std(nalive)

        print 'average living bears after 150 years: ',meanliving,' +/- ',stddev

#for i in range(nruns):
 #   bears = createpop.createpop(nyears)
  #  print 'Number of Living Male Bears: ',len(bears['alive']['male'])
   # print 'Number of Living Female Bears: ',len(bears['alive']['female'])
    #print 'Number of Dead Bears: ',len(bears['dead']['male'])+len(bears['dead']['female'])
    


