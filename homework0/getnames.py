def getnames():

    """ query government census webpage (or files) to get names. takes no inputs, return two lists: female names & male names """

    urlok = True

    if urlok == True:
        # import name lists from urls

        import urllib2

        furl="http://www.census.gov/genealogy/names/dist.female.first"
        murl="http://www.census.gov/genealogy/names/dist.male.first"

        fsite=urllib2.urlopen(furl)
        msite=urllib2.urlopen(murl)

    else:
        # if urlopen is not working, can also read from name lists from file

        fsite=open('fnames.txt','r')
        msite=open('mnames.txt','r')

    fnames=[line.split()[0] for line in fsite]
    mnames=[line.split()[0] for line in msite]

    return fnames, mnames

    
    
    
