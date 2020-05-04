import pickle
import os
from scipy.io.wavfile import read,write
from audio_matcher import *
import config

if __name__ == "__main__":
    db_dir = config.get("dbOutputDir")
    db_file = os.path.join(db_dir, "db.pickle")
    song_file = os.path.join(db_dir, "metadata.pickle")
    db = None
    songs = None
    
    with open(db_file,'rb') as f:
        db = pickle.load(f)
    
    with open(song_file,'rb') as f:
        songs = pickle.load(f)
    
    test_folder = config.get("testSongDir")
    test_files = os.listdir(test_folder)
    
    for tf in test_files:
        print(tf)
        rate,audio = read(os.path.join(test_folder, tf))
        audio = audio[0:rate*5]
        result = match(audio,rate,db,songs)
        print('song', result['song'], 'matched', result['matched'], 'start', result['start'])
    

    
    
