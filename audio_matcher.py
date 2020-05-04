import numpy as np
from scipy.io.wavfile import read,write
import numpy as np
import subprocess
import os
import pickle
import progressbar
from scipy.signal import lfilter,butter,hamming,blackman
from numba import jit
import config
import fingerprint

@jit(nopython=True)
def equal(c1,c2):
    hit = 0
    for i in range(c1.shape[0]):
        if abs(c1[i] - c2[i]) < 3:
            hit += 1
    
    if hit >= 3:
        return True
    else:
        return False

def match_chunk(chunk,db):
    matches = {}
    for s_code,fp in db.items():
        for i,fp_sec in enumerate(fp):
            if equal(chunk,fp_sec):
                matches.setdefault(s_code,[]).append(i)
    return matches

def match(audio,rate,db,songs):
    
    fp = fingerprint.fingerprint_song(audio,rate)
    l = int(fp.shape[0])
    candidates1 = match_chunk(fp[0],db)
    max_match_percent = 0
    matched_song = -1
    best_start = -1
    
    for code,start in candidates1.items():
        for s in start:
            hit = 1
            stop = l if l < (songs[code][1] - s) else songs[code][1] - s
            #print('s',s,'stop',stop)

            for i in range(1,stop):
                fp_i = fp[i]
                if(equal(fp_i,db[code][s+i])):
                    hit += 1
            match = (hit/l)*100
            if match > max_match_percent:
                max_match_percent = match
                best_start = s
                matched_song = code

    return {
        'song' : songs[matched_song][0],
        'matched' : max_match_percent,
        'start' : best_start
    }
