import numpy as np
from numba import jit
from scipy.signal import lfilter, butter, hamming, blackman
import config


@jit(nopython=True)
def downsample(song):
    ans = np.empty(shape=(int(song.shape[0] / 4)))
    j = 0
    for i in range(0, song.shape[0], 4):
        ans[j] = song[i : i + 4].mean()
        j += 1

    return ans


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype="low", analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


def convolve_hamming(song, n_samples):
    h = blackman(n_samples)
    for i in range(int(song.shape[0] / n_samples)):
        song[i * n_samples : (i + 1) * n_samples] = (
            song[i * n_samples : (i + 1) * n_samples] * h
        )
    return song


def convolve_fft(song, n_samples):
    ft = np.empty(shape=(int(song.shape[0] / n_samples), 512))
    for i in range(int(song.shape[0] / n_samples)):
        tmp = np.fft.fft(song[i * n_samples : (i + 1) * n_samples])
        ft[i] = 2 * np.sqrt(tmp.real ** 2 + tmp.imag ** 2)[0 : int(n_samples / 2)]
    return ft


def fingerprint(ft, song_id=None):
    time_freq_points = get_time_freq_points(ft)
    db = {}
    for index, point in enumerate(time_freq_points):
        start = max(index - 4, 0)
        end = (
            index
            if (index + 4) < len(time_freq_points)
            else (len(time_freq_points) - 5)
        )
        for target_zone_start_point in range(start, end + 1):
            anchor_point = target_zone_start_point - 3
            if anchor_point >= 0 and anchor_point < len(time_freq_points):
                address = (
                    time_freq_points[anchor_point][1],
                    point[1],
                    point[0] - time_freq_points[anchor_point][0],
                )

                if song_id != None:
                    value = (time_freq_points[anchor_point][0], song_id)
                else:
                    value = (time_freq_points[anchor_point][0])

                if address in db:
                    db[address].append(value)
                else:
                    db[address] = [value]
    return db


def get_time_freq_points(ft):
    time_freq_points = []
    for i, ft_i in enumerate(ft):
        frequencies = get_band_max(ft_i)
        frequencies.sort()
        for freq in frequencies:
            time_freq_points.append([i, freq])

    return time_freq_points


def get_band_max(ft):
    bin_boundries = [0, 10, 20, 40, 80, 160, 511]
    band_max = []
    s = 0
    for i in range(len(bin_boundries) - 1):
        max_freq = (
            np.argmax(ft[bin_boundries[i] : bin_boundries[i + 1]]) + bin_boundries[i]
        )
        band_max.append(max_freq)
        s += ft[max_freq]

    avg = s / (len(bin_boundries) - 1)
    thresold = avg * 0.75
    band_max = list(filter(lambda freq: ft[freq] >= thresold, band_max))
    return band_max


def remove_constant_freq(ft):
    j = 0

    for j in range(ft.shape[0]):
        u = len(np.unique(ft[j]))
        if u == 1:
            j += 1
        else:
            break
    return ft[j:]


def fingerprint_song(song, rate, song_id=None):
    cutoff_freq = config.get("cutofffreq")
    order_of_filter = config.get("filterOrder")
    window_size = config.get("windowSize")

    song = song[0 : int(song.shape[0] / window_size) * window_size]
    low_pass = butter_lowpass_filter(song, cutoff_freq, rate, order_of_filter)

    if rate == 44100:
        ds_song = downsample(low_pass)
    else:
        ds_song = low_pass
    hamming_song = convolve_hamming(ds_song, window_size)
    ft = convolve_fft(hamming_song, window_size)
    ft = remove_constant_freq(ft)

    return fingerprint(ft, song_id)