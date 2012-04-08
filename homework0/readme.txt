# Katherine de Kleer
# Homework 0 readme

1. To simply create a bear population over 150 years:

>run createpop
>bears = createpop(150)

This returns nested dictionaries: {'alive':{'male':[],'female':[]},'dead':{'male':[],'female':[]}}
containing all the bear instances in each of those categories.

2. To answer the questions:

>run answerqs
>answerqs('aa')

Allowed inputs:
'aa' - prints answer to first half of question a
example output: >average births:  8591.59  +/-  3642.39375986
'ab' - prints answer to second half of question a


Notes:
1. If urlopen fails (from too many queries?), go into getnames.py and change keyword urlok from True to False. This will tell it to read from file instead.
2. I played around with parts b & c but do not yet have a successful version
