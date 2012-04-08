# Katherine de Kleer
# 3/9/12
# AY250 homework#5

import sqlite3
import urllib2
from bs4 import BeautifulSoup
import csv
import os
import datetime
import time
import matplotlib.pyplot as plt
import numpy as np

""" predictelections: uses election data from intrade.com in .csv format to create a database of election probabilities for 2012 Presidential Election and Republican Presidential and Vice-Presidential Nomination. Crawls Wikipedia to get personal information about the candidates (stored in candidates.db) and download photos of each candidate (stored in a directory pictures/). Creates plots of (1) the probability of an Obama win versus a non-Republican win (2-4) the probability of a northern versus southern candidate victory in each of the three races """

# create table "races"
connection = sqlite3.connect("races.db")
cursor = connection.cursor()
sql_cmd = """CREATE TABLE races (rid INTEGER PRIMARY KEY AUTOINCREMENT,
    race_name TEXT, election_date DATE, data_url HYPERLINK)"""
cursor.execute(sql_cmd)

# populate table "races"
election_data = [
    ("2012 Republican Presidential Nomination", "8/30/12", "http://www.intrade.com/v4/markets/?eventId=84328"), 
    ("2012 Presidential Election", "12/17/12", "http://www.intrade.com/v4/markets/?eventId=84326"), 
    ("2012 Republican Vice-Presidential Nomination", "8/30/12", "http://www.intrade.com/v4/markets/?eventId=90482")]
for race in election_data:
    sql_cmd = ("INSERT INTO races (race_name, election_date, data_url) VALUES " + str(race))
    cursor.execute(sql_cmd)

# parse titles of csv files to get candidate names
dir='race_prediction_data/'
subdir=os.listdir(dir)
for item in subdir:
    if item[0]=='.':
        subdir.remove(item)
candidates = [item.split('_') for item in subdir]
candidates = [[entry[1],entry[0],entry[-1]] for entry in candidates] # creates list [lastname,firstname,race]
candidates.sort()

# create lists of candidates for each race
RepNom = []
RepVPNom = []
PresElect = []
allcand = []
for entry in candidates:
    if ([entry[0],entry[1]]) not in allcand:
        allcand.append([entry[0],entry[1]])
    if entry[2]=='RepNom.csv':
        RepNom.append([entry[0],entry[1]])
    if entry[2]=='RepVPNom.csv':
        RepVPNom.append([entry[0],entry[1]])
    if entry[2]=='PresElect.csv':
        PresElect.append([entry[0],entry[1]])

# create table "candidates"
connection2 = sqlite3.connect("candidates.db")
cursor2 = connection2.cursor()
sql_cmd = """CREATE TABLE candidates (cid INTEGER PRIMARY KEY AUTOINCREMENT,
    last_name TEXT, first_name TEXT, home_town TEXT, home_state TEXT, 
    party_affil TEXT, birth_date DATE, picture_link HYPERLINK)"""
cursor2.execute(sql_cmd)

# create opener
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

print '%PREDICT ELECTIONS: crawling wikipedia & parsing html'
for entry in allcand:
    # crawl wikipedia, pull data

    outfile=entry[1]+'_'+entry[0]+'.jpg'
    search_name = entry[1]+'_'+entry[0]

    # reformat select candidates
    if [entry[0],entry[1]] == ['West','Allen']:
        search_name = 'Allen_West_(politician)'
    if [entry[0],entry[1]] == ['Bolton','John']:
        search_name = 'John_R._Bolton'
    if [entry[0],entry[1]] == ['Huntsman','Jon']:
        search_name = 'Jon_Huntsman,_Jr.'
    if [entry[0],entry[1]] == ['Graham','Lindsay']:
        search_name = 'Lindsey_Graham'

    # open wikipedia page and grab thml data
    wikipage = 'http://en.wikipedia.org/w/index.php?title='+search_name+'&printable=yes'   
    infile=opener.open(wikipage)
    page=infile.read()
    soup = BeautifulSoup(''.join(page))
    trlist = soup.findAll('tr')

    skip = True
    gotbday=False
    gotparty=False
    gotpic=False
    for line in trlist:
        if (gotbday==False) and ('bday' in str(line)):
            # get birthday
            if ('Biden' in entry) and (skip==True):
                # special case: skip first birthday listing
                skip=False
                continue
            if 'title' in str(line):
                # parse various formatting cases for birthdate, hometown, and homestate
                birthdate = str(line).split('bday">')[1].split('</span>')[0]
                gotbday = True
                homeline1 = str(line).split('bday">')[1].split('title')
                if len(homeline1)==2:
                    homeline1=homeline1[-1]
                    if (homeline1[0]+homeline1[1])=='="':
                        hometown=homeline1.split('="')[1].split(',')[0].split('"')[0]
                        homestate=homeline1.split('="')[1].split(', ')[1].split('">')[0].split('<')[0]
                else: 
                    if len(homeline1)==3:
                        hometown=homeline1[-2].split('=>')[0].split('="')[1].split(',')[0].split('">')[0]
                        homestate=homeline1[-1].split('=>')[0].split('="')[1].split(',')[0].split('">')[0]
                        if 'United' in homestate:
                            homestate=homeline1[-2].split('=>')[0].split('="')[1].split(', ')[1].split('">')[0]
                    else:
                        if len(homeline1)==4:
                            hometown=homeline1[-3].split('=>')[0].split('="')[1].split(',')[0].split('">')[0]
                            homestate=homeline1[-3].split('=>')[0].split('="')[1].split(', ')[1].split('">')[0]
            else: 
                birthdate = str(line).split('bday">')[1].split('</span>')[0].split()[0]
                gotbday = True
                hometown = str(line).split('U.S.')[-2].split(',')[1].split('\n')[-1]
                homestate = str(line).split('U.S.')[-2].split(', ')[-2]
            if ('New York' in homestate) or ('Long Island' in homestate):
                homestate = 'New York'
        if ('Political party' in str(line)) and (gotparty==False):
            # parse and collect political party affiliation
            affiliation = 'none'
            if 'title' in str(line):
                affiliation = str(line).split('title="')[1].split('">')[1].split('</a>')[0]
            else:
                affiliation = str(line).split('<td')[1].split('>')[0]
            # standardize political party formatting
            if ('Republican' in affiliation):
                affiliation = 'Republican'
            if ('Democrat' in affiliation.split(' ')[0]):
                affiliation = 'Democrat'
            if (affiliation=='' or affiliation=='none'):
                affiliation = 'Independent'
            gotparty=True

    # TO DOWNLOAD IMAGES, UNCOMMENT THE FOLLOWING [a directory called pictures/ must be present in this directory]
    #if ('.jpg' in str(line)) and (gotpic==False):
        #   picurl='http:'+str(line).split('src="')[1].split('"')[0]
        #   picfile = opener.open(picurl)
        #   picpage = picfile.read()
        #   output = open('pictures/'+outfile,'wb')
        #   output.write(picpage)
        #   output.close()
        #   gotpic=True

    # populate table "candidates"
    sql_cmd = ("INSERT INTO candidates (last_name, first_name, home_town, home_state, " +
               "party_affil, birth_date, picture_link) VALUES " + str(tuple([entry[0],entry[1],hometown,homestate,affiliation,birthdate,outfile])))
    cursor2.execute(sql_cmd)

# create table "predictions"
connection3 = sqlite3.connect("predictions.db")
cursor3 = connection3.cursor()
sql_cmd = """CREATE TABLE predictions (pid INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE, price FLOAT, volume INTEGER, cid INTEGER, rid INTEGER)"""
cursor3.execute(sql_cmd)

print '%PREDICT ELECTIONS: reading .csv datafiles'
# read data from .csv files from intrade.com
for csvfile in subdir:
    spamReader = csv.reader(open('race_prediction_data/'+csvfile, 'rb'))
    first=csvfile.split('/')[-1].split('.csv')[-2].split('_')[0]
    last=csvfile.split('/')[-1].split('.csv')[-2].split('_')[1]
    race=csvfile.split('/')[-1].split('.csv')[-2].split('_')[-1]
    cand=[last,first]
    races=['RepNom','PresElect','RepVPNom']
    rid = races.index(race)+1
    cid = allcand.index(cand)+1
    firstrow=True
    for row in spamReader:
        if firstrow==False:
            date = row[0]
            price = row[-2]
            volume = row[-1]
            entry=[date,price,volume,cid,rid]
            # populate "predictions" table
            sql_cmd=("INSERT INTO predictions (date, price, volume, cid, rid) VALUES " + str(tuple(entry)))
            cursor3.execute(sql_cmd)
        else:
            firstrow=False

# defines the states in the south versus the north based on location of the Mason-Dixon line
thesouth=['West Virginia', 'Maryland', 'Virginia', 'North Carolina', 'Kentucky', 'Tennessee', 'Mississippi', 'Alabama', 'Georgia', 'South Carolina', 'Florida', 'Arkansas', 'Louisiana', 'Texas', 'Oklahoma']
thenorth=['Pennsylvania', 'New York', 'Delaware', 'New Jersey', 'Rhode Island', 'Massachusetts', 'Vermont', 'New Hampshire', 'Connecticut', 'Maine', 'Minnesota', 'Wisconsin', 'Iowa', 'Missouri', 'Nebraska', 'Illinois', 'Indiana', 'Michigan', 'Ohio']

southids = []
# get IDs for candidates from the south
for state in thesouth:
    sql_cmd = "SELECT * FROM candidates where home_state = '"+state+"'"
    cursor2.execute(sql_cmd)
    db_info = cursor2.fetchall()
    for entry in db_info: 
        cid=entry[0]
        southids.append(cid)
northids = []
# get IDs for candidates from the north
for state in thenorth:
    sql_cmd = "SELECT * FROM candidates where home_state = '"+state+"'"
    cursor2.execute(sql_cmd)
    db_info = cursor2.fetchall()
    for entry in db_info: 
        cid=entry[0]
        northids.append(cid)

# create array of every date within the past year
startdate = datetime.date(2011,3,5) # get one year's worth of data
enddate = datetime.date(2012,3,5)
day_count = (enddate - startdate).days + 1
alldates=[]
for single_date in [d for d in (startdate + datetime.timedelta(n) for n in range(day_count)) if d <= enddate]:
    s = single_date.strftime("%b %d, %Y")
    if single_date.day < 10:
        s=s[:4]+s[5:]
    alldates.append(s)

# create list of Republican candidate IDs
sql_cmd = "SELECT * FROM candidates where party_affil='Republican'"
cursor2.execute(sql_cmd)
db_info=cursor2.fetchall()
repubid = []
for entry in db_info: 
    repubid.append(entry[0])

print '%PREDICT ELECTIONS: determining presidential win probabilities'
# create list of probabilities for Republican wins per day
repubprob=[]
currentprob=np.zeros(len(repubid))       
for day in alldates:
    count = 0.
    for i in range(len(repubid)):
        cand = repubid[i]
        sql_cmd="SELECT * FROM predictions where cid = "+str(cand)+" and date = '"+day+"' and rid = "+str(2)
        cursor3.execute(sql_cmd)
        db_info = cursor3.fetchall()
        if db_info != []:
            prob = (db_info[0][2])*.01
            currentprob[i] = prob
        count += currentprob[i]
    repubprob.append(count)

# create list of probabilities for an Obama win
currentprob=0.     
obamaprob = []
for day in alldates:
    count = 0.
    sql_cmd = "SELECT * FROM candidates where last_name='Obama'"
    cursor2.execute(sql_cmd)
    db_info = cursor2.fetchall()
    obamaid = db_info[0][0]
    sql_cmd="SELECT * FROM predictions where cid = "+str(obamaid)+" and date = '"+day+"' and rid = "+str(2)
    cursor3.execute(sql_cmd)
    db_info = cursor3.fetchall()
    if db_info != []:
        prob = (db_info[0][2])*.01
        currentprob = prob
    count += currentprob
    obamaprob.append(count)

# convert list of dates into date objects for plotting
dateobjs = []
for date in alldates:
    newtime = time.strptime(date,"%b %d, %Y")
    newdate = datetime.date(newtime.tm_year,newtime.tm_mon,newtime.tm_mday)
    dateobjs.append(newdate)

# create non-Republican versus Obama victory plot
plt.plot(dateobjs,[1-i for i in repubprob],label='non-Republican win')
plt.plot(dateobjs,obamaprob,label='Obama win')
plt.title('Victory Probability for 2012 Presidential Election')
plt.legend()
plt.show()

# calculate probabilities of north versus south winning in all three races
southprobRNom = []
northprobRNom = []
southprobPres = []
northprobPres = []
southprobRVPNom = []
northprobRVPNom = []
print '%PREDICT ELECTIONS: determining north vs. south presidential nomination probabilities'
for day in alldates:
    southcount = 0.
    for cand in southids:
        currentprob = 0.
        sql_cmd="SELECT * FROM predictions where cid = "+str(cand)+" and date = '"+day+"' and rid = "+str(1)
        cursor3.execute(sql_cmd)
        db_info = cursor3.fetchall()
        if db_info != []:
            prob = (db_info[0][2])*.01
            southcount += prob
    southprobRNom.append(southcount)
for day in alldates:
    northcount = 0.
    for cand in northids:
        sql_cmd="SELECT * FROM predictions where cid = "+str(cand)+" and date = '"+day+"' and rid = "+str(1)
        cursor3.execute(sql_cmd)
        db_info = cursor3.fetchall()
        if db_info != []:
            prob = (db_info[0][2])*.01
            northcount += prob
    northprobRNom.append(northcount)
print '%PREDICT ELECTIONS: determining north vs. south presidential win probabilities'
for day in alldates:
    southcount = 0.
    for cand in southids:
        currentprob = 0.
        sql_cmd="SELECT * FROM predictions where cid = "+str(cand)+" and date = '"+day+"' and rid = "+str(2)
        cursor3.execute(sql_cmd)
        db_info = cursor3.fetchall()
        if db_info != []:
            prob = (db_info[0][2])*.01
            southcount += prob
    southprobPres.append(southcount)
for day in alldates:
    northcount = 0.
    for cand in northids:
        sql_cmd="SELECT * FROM predictions where cid = "+str(cand)+" and date = '"+day+"' and rid = "+str(2)
        cursor3.execute(sql_cmd)
        db_info = cursor3.fetchall()
        if db_info != []:
            prob = (db_info[0][2])*.01
            northcount += prob
    northprobPres.append(northcount)
print '%PREDICT ELECTIONS: determining north vs. south vice-presidential nomination probabilities'
for day in alldates:
    southcount = 0.
    for cand in southids:
        currentprob = 0.
        sql_cmd="SELECT * FROM predictions where cid = "+str(cand)+" and date = '"+day+"' and rid = "+str(3)
        cursor3.execute(sql_cmd)
        db_info = cursor3.fetchall()
        if db_info != []:
            prob = (db_info[0][2])*.01
            southcount += prob
    southprobRVPNom.append(southcount)
for day in alldates:
    northcount = 0.
    for cand in northids:
        sql_cmd="SELECT * FROM predictions where cid = "+str(cand)+" and date = '"+day+"' and rid = "+str(3)
        cursor3.execute(sql_cmd)
        db_info = cursor3.fetchall()
        if db_info != []:
            prob = (db_info[0][2])*.01
            northcount += prob
    northprobRVPNom.append(northcount)

# make north versus south figures
f=plt.figure()
plt.plot(dateobjs,southprobRNom,label='The South')
plt.plot(dateobjs,northprobRNom,label='The North')
plt.title('Probability of Victory in Republican Presidential Nomination 2012')
plt.legend()
plt.show()

f=plt.figure()
plt.plot(dateobjs,southprobPres,label='The South')
plt.plot(dateobjs,northprobPres,label='The North')
plt.title('Probability of Victory in Presidential Election 2012')
plt.legend()
plt.show()

f=plt.figure()
plt.plot(dateobjs,southprobRVPNom,label='The South')
plt.plot(dateobjs,northprobRVPNom,label='The North')
plt.title('Probability of Victory in Republican Vice-Presidential Nomination 2012')
plt.legend()
plt.show()
    




