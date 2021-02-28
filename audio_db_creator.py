from scipy.io.wavfile import read, write
import numpy as np
import subprocess
import os
import pickle
import config
from audio_matcher import *
import songs
import fingerprint


def merge(main_dict, dict_to_add):
    for k, v in dict_to_add.items():
        if k in main_dict:
            main_dict[k].extend(v)
        else:
            main_dict[k] = v


if __name__ == "__main__":

    raw_song_dir = config.get("rawSongDir")
    db_dir = config.get("dbOutputDir")
    raw_songs = os.listdir(raw_song_dir)

    song_codes = {}
    code = 0
    db = {}

    for s in raw_songs:
        print(s)

        processed = songs.pre_process(os.path.join(raw_song_dir, s))

        if processed is None:
            print(s, "file not supported")
            continue

        rate, song = processed

        if song.dtype == np.int16 and rate == 44100:
            print(s, ": ACCEPTED")
            fp = fingerprint.fingerprint_song(song, rate, code)
            merge(db, fp)
            song_codes[code] = s
            code += 1
        else:
            print(s, ": REJECTED", song.dtype, rate, song.shape)

    f = open(os.path.join(db_dir, "db.pickle"), "wb")
    pickle.dump(db, f)
    f.close()

    f = open(os.path.join(db_dir, "metadata.pickle"), "wb")
    pickle.dump(song_codes, f)
    f.close()
