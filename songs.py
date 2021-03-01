import config
import subprocess
import os
import numpy as np
from scipy.io.wavfile import read


def convert_to_wav(filepath):
    path_to_ffmpeg = config.get("pathToFfmpeg")
    _, file_format = os.path.splitext(filepath)

    if file_format == ".mp3":
        name_without_extension = os.path.basename(filepath).split(file_format)[0]
        output_file = os.path.join(
            os.path.dirname(filepath), name_without_extension + ".wav"
        )
        ret = subprocess.call([path_to_ffmpeg, "-i", filepath, output_file])
        if ret >= 0:
            return output_file
        else:
            return None
    elif file_format == ".wav":
        return filepath
    else:
        return None


def stereo_to_mono(song):
    if song.ndim == 1:
        song = np.reshape(song, (song.shape[0], 1))
    elif song.shape[1] == 2:
        song = song.astype(np.int)
        song = (song.sum(axis=1) / 2).astype(np.int16)
    return song

def validate_song(song, rate):
    return song.dtype == np.int16 and rate == 44100

def pre_process(file):
    wav_file = convert_to_wav(file)

    if wav_file is None:
        return None

    rate, song = read(wav_file)
    return rate, stereo_to_mono(song)
