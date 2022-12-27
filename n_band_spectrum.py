import time 
import sys
import os
import numpy as np
import wave
import pyaudio
import Audio_equalizer

files = [r"C:\Users\Gmusl\Desktop\Python Scripts\rickroll.wav", r"C:\Users\Gmusl\Desktop\Python Scripts\voice.wav", r"C:\Users\Gmusl\Desktop\Python Scripts\jump.wav", r"C:\Users\Gmusl\Desktop\Python Scripts\drake.wav", r"C:\Users\Gmusl\Desktop\Python Scripts\metro.wav"]


def display_4_band(band1, band2, band3, band4):
    print(f"band1: {band1}  band2: {band2}  band3: {band3}  band4: {band4}")
    for i in range(10, 0, -1):
        txt = ""
        if band1 >= i:
            txt += " | "
        else:
            txt += "   "
        if band2 >= i:
            txt += " | "
        else:
            txt += "   "
        if band3 >= i:
            txt += " | "
        else:
            txt += "   "
        if band4 >= i:
            txt += " | "
        else:
            txt += "   "
        print(txt)
def display_n_band(bands):
    num_bands = len(bands)
    for i in range(10, 0, -1):
        txt = ""
        
        for j in range(num_bands):
            if bands[j] >= i:
                txt += " | "
            else:
                txt += "   "
        print(txt)
def countdown(n_seconds):
    while n_seconds > 0:
        print(n_seconds)
        time.sleep(1)
        n_seconds -= 1


def playAudio(song_filepath :str, write_data=True, num_bands = 5, custom_bands=[], showPlots=False, countdown_time=0):
    """Show graphic audio equalizer of song at song_filepath.\n
    Function will write data to two files, one containing the band data \n
    and another containing time segmentation data, where time differences are shown in ms.\n

    Custom bands should be in the form [num1, num2, num3, num4] where num1--num2 is one band and num2--num3 is another.\n
    numX refers to the corner frequency of a particular band.
    """

    band_data, time_data = [],[]
    if write_data:
        band_data, time_data = Audio_equalizer.nBandEq(song_filepath, num_bands,showPlots=showPlots, customBands=custom_bands)

    else: #read from text files
        with open("band_data.txt", "r") as infile:
            lines = infile.readlines()
            for line in lines:
                band_data.append(eval(line))
            time.sleep(1)

    band_data = np.abs(band_data)
    band_data = np.array([[int(p) for p in i] / np.average(i) * 4 for i in band_data], dtype=np.int8)

    wf = wave.open(song_filepath, "rb")

    # instantiate PyAudio
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    chunk = 3000
    num_frame = 0

    if write_data:
        #only extract useful frames from band_data
        tmp = [[] for _ in band_data]
        for i in range(len(tmp)): #loop through bands
            for j in range(len(band_data[i])):
                if j % chunk == 0:
                    tmp[i].append(band_data[i][j])
        band_data = tmp
        with open("band_data.txt", "w") as outfile: #write data to files
            for band in band_data:
                outfile.write(str(band) + "\n")
        with open("time_data.txt", "w") as outfile:
            count = 5
            for i in range(len(time_data)):
                if i % chunk == 0:
                    outfile.write(str(int(time_data[i] * 1000)) + "\n")
                    count -= 1
                if count <= 0:
                    break

    data = wf.readframes(chunk)

    countdown(countdown_time)
    while data != '':
        os.system("cls")
        try:
            display_n_band([i[num_frame] for i in band_data])
        except:
            print("song finished!")
            break
        stream.write(data)
        data = wf.readframes(chunk)
        num_frame += 1
        
    stream.close()
    p.terminate()

playAudio(files[2],num_bands=10, countdown_time=3)