import pickle
import os
from audio_matcher import *
import config
import argparse

def read_dict(file_path):
    data = None
    with open(file_path, "rb") as f:
        data = pickle.load(f)

    return data

# TODO
# 1) Take command line args // done
# 2) Fix file reading issue // done
# 3) Test with more songs
# 4) Document code
# 5) Make GIF
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("recording", help="path to the recording")
    args = parser.parse_args()
    test_file = os.path.abspath(args.recording)
    
    db_dir = config.get("dbOutputDir")
    db_file = os.path.join(db_dir, "db.pickle")
    song_file = os.path.join(db_dir, "metadata.pickle")
    db = read_dict(db_file)
    songs_metadata = read_dict(song_file)

    song_code, err_msg = match(test_file, db)
    
    if song_code != -1:
        print("song is : ", songs_metadata[song_code])
    else:
        print("No match found")
