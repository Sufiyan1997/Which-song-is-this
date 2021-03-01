import os
import pickle
import config
import songs
import fingerprint
import argparse


def merge(main_dict, dict_to_add):
    for k, v in dict_to_add.items():
        if k in main_dict:
            main_dict[k].extend(v)
        else:
            main_dict[k] = v

def save_dict(file_path, dictionary):
    f = open(file_path, "wb")
    pickle.dump(dictionary, f)
    f.close()

def create_db(song_list):
    song_codes = {}
    code = 0
    db = {}

    for song_filepath in song_list:
        print(song_filepath)

        processed = songs.pre_process(song_filepath)

        if processed is None:
            print(song_filepath, "file not supported")
            continue

        rate, song = processed

        if songs.validate_song(song, rate):
            print(song_filepath, ": ACCEPTED")
            fp = fingerprint.fingerprint_song(song, rate, code)
            merge(db, fp)
            song_codes[code] = os.path.basename(song_filepath)
            code += 1
        else:
            print(song_filepath, ": REJECTED", song.dtype, rate, song.shape)

    print("-"*10+"REPORT"+"-"*10)
    print(str(code) + "songs added to db.")

    return db, song_codes

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="Path to directory which has songs to be added in db")
    parser.add_argument("output", help="path to directory where db files will be stored")
    args = parser.parse_args()

    raw_song_dir = os.path.abspath(args.source)
    db_dir = os.path.abspath(args.output)
    print(raw_song_dir)
    print(db_dir)
    raw_songs = [os.path.join(raw_song_dir, s) for s in os.listdir(raw_song_dir)]

    db, song_codes = create_db(raw_songs)

    save_dict(os.path.join(db_dir, "db.pickle"), db)
    save_dict(os.path.join(db_dir, "metadata.pickle"), song_codes)
