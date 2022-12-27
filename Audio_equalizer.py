import wave
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


#humans sensitive to 250-5k Hz
def bandpass(corners, signal_array, framerate):
    band = signal.butter(2, corners, 'bandpass', fs=framerate, output='sos')
    filtered_signal = signal.sosfilt(band, signal_array)
    return filtered_signal
def get5BandAudioData(audio_file, showPlots=False):
    bands = []
    sound = wave.open(audio_file)
    frames = sound.readframes(-1)
    sound_len = sound.getnframes() / sound.getframerate()
    print(sound.getsampwidth())
    signal_arr = np.frombuffer(frames, dtype=np.int16)
    time_arr = np.linspace(0, sound_len, num=sound.getnframes())
    bands.append(bandpass([1, 40], signal_arr, sound.getframerate()))
    bands.append(bandpass([40, 80], signal_arr, sound.getframerate()))
    bands.append(bandpass([80, 150], signal_arr, sound.getframerate()))
    bands.append(bandpass([150, 151], signal_arr, sound.getframerate()))
    if showPlots:
        fig, ax = plt.subplots(5, 1)
        
        ax[0].plot(time_arr, signal_arr)
        ax[0].set_title("signal")
        ax[1].plot(time_arr, bands[0])
        ax[1].set_title("band 1")
        ax[2].plot(time_arr, bands[1])
        ax[2].set_title("band 2")
        ax[3].plot(time_arr, bands[2])
        ax[3].set_title("band 3")
        ax[4].plot(time_arr, bands[3])
        ax[4].set_title("band 4")
        fig.tight_layout()
        plt.show()

    return bands, time_arr
def nBandEq(audio_file :str, n_bands=2, showPlots=False, customBands=[]):
    """Audio equalizer consisting of n bands.
    """
    bands = []
    choices = [1, 40, 60, 100, 150, 300, 600, 1000, 3000, 6000, 12000]
    if len(customBands) != 0:
        choices = customBands
    sound = wave.open(audio_file)
    frames = sound.readframes(-1)
    sound_len = sound.getnframes() / sound.getframerate()
    signal_arr = np.frombuffer(frames, dtype=np.int32)
    time_arr = np.linspace(0, sound_len, num=sound.getnframes())
    for i in range(len(choices) - 1):
        bands.append(bandpass([choices[i], choices[i+1]], signal_arr, sound.getframerate()))
    if showPlots:
        fig, ax = plt.subplots(n_bands+1, 1, figsize=(10, 12))
        ax[0].plot(time_arr, signal_arr)
        ax[0].set_title("signal")
        for i in range(n_bands):
            ax[i+1].plot(time_arr, bands[i])
            ax[i+1].set_title(f"band {i}")
        fig.tight_layout()
        plt.show()
    return bands[:n_bands], time_arr
    
