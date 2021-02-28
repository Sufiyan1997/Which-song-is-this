import pickle
import os
from scipy.io.wavfile import read, write
from audio_matcher import *
import config
import songs

if __name__ == "__main__":
    db_dir = config.get("dbOutputDir")
    db_file = os.path.join(db_dir, "db.pickle")
    song_file = os.path.join(db_dir, "metadata.pickle")
    db = None
    songs_metadata = None

    with open(db_file, "rb") as f:
        db = pickle.load(f)

    with open(song_file, "rb") as f:
        songs_metadata = pickle.load(f)

    test_folder = config.get("testSongDir")
    test_files = os.listdir(test_folder)

    for tf in test_files:
        print(tf)
        song_code, err_msg = match(os.path.join(test_folder, tf), db)
        
        if song_code != -1:
            print("song is : ", songs_metadata[song_code])
        else:
            print("No match found")
