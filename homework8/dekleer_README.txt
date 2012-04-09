Katherine de Kleer
AY250 homework 8 README
4/8/12

Files:
create_db.py [located in homework5 folder]
parse_db.py [located in homework8 folder]
changelog.txt

> python parse_db.py -h
usage: parse_db.py [-h] [-c CANDIDATE] [-d DATE] [-p]

Election_Database

optional arguments:
  -h, --help    show this help message and exit
  -c CANDIDATE  Enter last or full name of candidate
  -d DATE       Date of interest, format=YYYY-MM-DD
  -p            Set flag to plot prediction over time

example:
> python parse_db.py -c Bush -p -d 2012-02-04
Feb 4, 2012 | Bush for Republican Presidential Nomination: 0.5%
Feb 4, 2012 | Bush for Republican Vice-Presidential Nomination: 0.7%

Notes:
I don't have a lot of commits for my research work -- I don't have a lot of time for research as a first year, and didn't feel like inventing commits for this assignment.


