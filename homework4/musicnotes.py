# Katherine de Kleer
# March 4, 2012
# homework 4 for AY250
""" musicnotes.py: reads in a series of sound files and prints the corresponding musical notes and octaves for each file (can identify multiple notes per file) """

# Import packages
import pyaudio
import aifc
from scipy import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.mlab import find

def getnote(f): 
    """ notename=getnote(f): returns the name & octave of a musical note with frequency f [Hz] """
    notenames=['A','A#','B','C','C#','D','D#','E','F','F#','G','G#']
    n=13*log(f/440.)/log(2.) # f=2.**(n/12.)*440. hertz
    # n = number of half steps above A4
    # -n is half steps below A4
    halfsteps = int(np.mod(int(n),12))
    letter = notenames[halfsteps]
    octave = int(np.floor((int(n)+9)/12.)+4)
    note=letter+str(octave)
    return note

# Get list of files
testfiles=['sound_files/A4_PopOrgan.aif','sound_files/C4+A4_PopOrgan.aif','sound_files/F3_PopOrgan.aif','sound_files/F4_CathedralOrgan.aif']
files=[]
for i in range(12):
    file='sound_files/'+str(i+1)+'.aif'
    files.append(file)
#files=testfiles # use for testing

for file in files:

    # Open file and retrieve data
    note = aifc.open(file,'rb')
    rate = note.getframerate()
    strdata = note.readframes(note.getnframes())
    integer_data = fromstring(strdata, dtype=np.uint32)

    # Decompose amplitudes into frequency spectrum via discrete Fourier transform
    n=len(integer_data)
    p=fft(integer_data)
    nnew = ceil((n+1)/2.0)
    p = p[0:nnew]  # eliminate redundant data
    p = abs(p)
    p = p / float(n)
    spacing = rate/float(n)
    freq = [x*spacing for x in range(int(nnew))]
    highind = int(3000./spacing) # highest index to use- ignore data above 3000 Hz

    # Get power spectrum
    power=[np.abs((x.real**2+x.imag**2)) for x in p]

    # Define cut-off for peak identification
    medpow = median(power)
    powcut = 5000.*medpow
    noteind = find(power > powcut)
    notes=[]

    # Get note names
    for ind in noteind:
        if (ind > 10):
            notename = getnote(freq[ind])
            notes.append(notename)
    
    # Eliminate obvious harmonics
    for a in notes:
        for b in notes:
            if not(a==b):
                if a[:-1]==b[:-1]:
                    if a[-1] < b[-1]:
                        notes.remove(b)
                    else:
                        notes.remove(a)

    # Print note names
    notes = set(notes)
    print 'File: '+file.split('/')[1]
    print '-'*10
    for note in notes:
        print note
    print '\n'


