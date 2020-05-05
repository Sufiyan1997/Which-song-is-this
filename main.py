import pickle
import os
from scipy.io.wavfile import read,write
from audio_matcher import *
import config
import songs

if __name__ == "__main__":
    db_dir = config.get("dbOutputDir")
    db_file = os.path.join(db_dir, "db.pickle")
    song_file = os.path.join(db_dir, "metadata.pickle")
    db = None
    songs_metadata = None
    
    with open(db_file,'rb') as f:
        db = pickle.load(f)
    
    with open(song_file,'rb') as f:
        songs_metadata = pickle.load(f)
    
    test_folder = config.get("testSongDir")
    test_files = os.listdir(test_folder)
    
    for tf in test_files:
        print(tf)
        processed = songs.pre_process(os.path.join(test_folder, tf))
        
        if processed is None:
            continue
        
        rate, audio = processed
        result = match(audio,rate,db,songs_metadata)
        print('song', result['song'], 'matched', result['matched'], 'start', result['start'])
    

    
    
