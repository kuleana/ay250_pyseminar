# Katherine de Kleer
# 4/8/12
# AY250 homework 8

import argparse
import pylab
import sys
import os
import sqlite3
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib

""" parse_db: using election data from intrade.com stored in sql databases, allows user to make convenient queries for the probability of a win for a given candidate over time, or on a given date. Optionally shows this in plot format as well """

# create databases if they do not already exist
if 'predictions.db' not in os.listdir('.'):
    createdb_loc="../homework5/"
    sys.path.append(createdb_loc)
    try:
        import create_db
    except:
        print "create_db.py not found in"+loc

# set up parser
parser=argparse.ArgumentParser(description='Election_Database')
parser.add_argument('-c',action='store',dest='candidate',
                    help='Enter last or full name of candidate')
parser.add_argument('-d',action='store',dest='date',
                    help='Date of interest, format=YYYY-MM-DD')
parser.add_argument('-p',action='store_true',default=False,dest='plot_data',
                    help='Set flag to plot prediction over time')
results=parser.parse_args()

connection2=sqlite3.connect("predictions.db")
cursor2=connection2.cursor()

# read in inputs and re-format
lastname=results.candidate
date_input=results.date

if (date_input != None):
    YY=int(date_input.split('-')[0])
    MM=int(date_input.split('-')[1])
    DD=int(date_input.split('-')[2])
    single_date=datetime.date(YY,MM,DD)
    s = single_date.strftime("%b %d, %Y")
    if single_date.day < 10:
        s=s[:4]+s[5:]
    sql_cmd = "SELECT * FROM predictions where name like '%"+str(lastname)+"%' and date = '"+s+"'"
else:
    sql_cmd = "SELECT * FROM predictions where name like '%"+str(lastname)+"%'"

cursor2.execute(sql_cmd)
db_info=cursor2.fetchall()
races=['Republican Presidential Nomination','Presidential Election','Republican Vice-Presidential Nomination']
for line in db_info:
    # output formatted information
    print line[1]+' | '+lastname+' for '+races[line[5]-1]+': '+str(line[2])+'%'

# make plot
if (results.plot_data == True):
    # select data over all time
    sql_cmd = "SELECT * FROM predictions where name like '%"+str(lastname)+"%'"
    cursor2.execute(sql_cmd)
    db_info=cursor2.fetchall()
    dates_reppres=[]
    values_reppres=[]
    dates_preselect=[]
    values_preselect=[]
    dates_repvp=[]
    values_repvp=[]
    for line in db_info:
        # parse plotting data for each race separately
        if line[5]==1:
            dates_reppres.append(datetime.datetime.strptime(line[1],"%b %d, %Y"))
            values_reppres.append((float(line[2])*.01))
        if line[5]==2:
            dates_preselect.append(datetime.datetime.strptime(line[1],"%b %d, %Y"))
            values_preselect.append((float(line[2])*.01))
        if line[5]==3:
            dates_repvp.append(datetime.datetime.strptime(line[1],"%b %d, %Y"))
            values_repvp.append((float(line[2])*.01))
    if len(dates_reppres) != 0:
        plt.plot(dates_reppres,values_reppres,label='Republican Presidential Nomination')
    if len(dates_preselect) != 0:
        plt.plot(dates_preselect,values_preselect,label='Presidential Election')
    if len(dates_reppres) != 0:
        plt.plot(dates_repvp,values_repvp,label='Republican Vice Presidential Nomination')
    if (date_input != None):
            # plot circles for the date indicated
            YY=int(date_input.split('-')[0])
            MM=int(date_input.split('-')[1])
            DD=int(date_input.split('-')[2])
            single_date=datetime.date(YY,MM,DD)
            s = single_date.strftime("%b %d, %Y")
            if single_date.day < 10:
                s=s[:4]+s[5:]
            dates_single=[]
            values_single=[]
            for line in db_info:
                if line[1]==s:
                    dates_single.append(single_date)
                    values_single.append(line[2]*.01)
            plt.plot(dates_single,values_single,'o')
    # format plot
    title='Probability of '+lastname+' Victory in 2012'
    plt.title(title)
    plt.legend()
    plt.show()
