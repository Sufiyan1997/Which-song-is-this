import numpy as np
from numba import jit
from scipy.signal import lfilter,butter,hamming,blackman
import config

@jit(nopython=True)
def downsample(song):
    ans = np.empty(shape=(int(song.shape[0]/4)))
    j = 0
    for i in range(0,song.shape[0],4):
        ans[j] = song[i:i+4].mean()
        j += 1

    return ans


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def convolve_hamming(song,n_samples):
    h = blackman(n_samples)
    for i in range(int(song.shape[0]/n_samples)):
        song[i*n_samples:(i+1)*n_samples] = song[i*n_samples:(i+1)*n_samples]*h
    return song

def convolve_fft(song,n_samples):
    ft = np.empty(shape=(int(song.shape[0]/n_samples),512))
    for i in range(int(song.shape[0]/n_samples)):
        tmp = np.fft.fft(song[i*n_samples:(i+1)*n_samples])
        ft[i] = 2*np.sqrt(tmp.real**2+tmp.imag**2)[0:int(n_samples/2)]
    return ft

def fingerprint(ft):
    bin_boundries = [0,10,20,40,80,160,511]
    band_max = []
    for i in range(len(bin_boundries)-1):
        band_max.append(np.argmax(ft[bin_boundries[i]:bin_boundries[i+1]])+bin_boundries[i])
    
    return band_max

def fingerprint_song(song,rate):
    cutoff_freq = config.get("cutofffreq")
    order_of_filter = config.get("filterOrder")
    window_size = config.get("windowSize")
    
    song = song[0:int(song.shape[0]/window_size)*window_size]
    low_pass = butter_lowpass_filter(song, cutoff_freq, rate, order_of_filter)
    
    if rate == 44100:
        ds_song = downsample(low_pass)
    else:
        ds_song = low_pass
    hamming_song = convolve_hamming(ds_song,window_size)
    ft = convolve_fft(hamming_song,window_size)
    j = 0
    
    for j in range(ft.shape[0]):
        u = len(np.unique(ft[j]))
        if u == 1:
            j+=1
        else:
            break
    ft = ft[j:]

    fp = np.empty(shape=(ft.shape[0],6))
    for i,fp_i in enumerate(ft):
        fp[i] = fingerprint(fp_i)
    return fp