import pickle
import os
from audio_matcher import *
import config

def read_dict(file_path):
    data = None
    with open(file_path, "rb") as f:
        data = pickle.load(f)

    return data

if __name__ == "__main__":
    db_dir = config.get("dbOutputDir")
    db_file = os.path.join(db_dir, "db.pickle")
    song_file = os.path.join(db_dir, "metadata.pickle")
    test_folder = config.get("testSongDir")
    test_files = os.listdir(test_folder)
    
    db = read_dict(db_file)
    songs_metadata = read_dict(song_file)

    for tf in test_files:
        print(tf)
        song_code, err_msg = match(os.path.join(test_folder, tf), db)
        
        if song_code != -1:
            print("song is : ", songs_metadata[song_code])
        else:
            print("No match found")
