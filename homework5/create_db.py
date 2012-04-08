# Katherine de Kleer
# 4/6/12
# AY250 homework#8
# modified from AY250 homework#5

import sqlite3
import urllib2
from bs4 import BeautifulSoup
import csv
import os
import datetime
import time
import matplotlib.pyplot as plt
import numpy as np

""" create_db: uses election data from intrade.com in .csv format to create a database of election probabilities for 2012 Presidential Election and Republican Presidential and Vice-Presidential Nomination."""

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

# create table "predictions"
connection3 = sqlite3.connect("predictions.db")
cursor3 = connection3.cursor()
sql_cmd = """CREATE TABLE predictions (pid INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE, price FLOAT, volume INTEGER, name TEXT, rid INTEGER)"""
cursor3.execute(sql_cmd)

print '%CREATE_DB: reading .csv datafiles'
# read data from .csv files from intrade.com
for csvfile in subdir:
    spamReader = csv.reader(open('race_prediction_data/'+csvfile, 'rb'))
    first=csvfile.split('/')[-1].split('.csv')[-2].split('_')[0]
    last=csvfile.split('/')[-1].split('.csv')[-2].split('_')[1]
    race=csvfile.split('/')[-1].split('.csv')[-2].split('_')[-1]
    cand=[last,first]
    races=['RepNom','PresElect','RepVPNom']
    rid = races.index(race)+1
    name = cand[1]+' '+cand[0]
    firstrow=True
    for row in spamReader:
        if firstrow==False:
            date = row[0]
            price = row[-2]
            volume = row[-1]
            entry=[date,price,volume,name,rid]
            # populate "predictions" table
            sql_cmd=("INSERT INTO predictions (date, price, volume, name, rid) VALUES " + str(tuple(entry)))
            cursor3.execute(sql_cmd)
        else:
            firstrow=False

connection.commit()
cursor.close()
connection3.commit()
cursor3.close()
