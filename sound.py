# Don't do import *! (It just makes this example smaller)
from pedalboard import *
from pedalboard.io import AudioFile
from pedalboard.pedalboard import Pedalboard
import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
import subprocess
from IPython.display import Audio
import base64



import simpleaudio as sa #permet de jouer des fichiers .wav directement dans python en executant le script



# Read in a whole file, resampling to our desired sample rate:
samplerate = 44100.0
with AudioFile('C:/Users/User/Documents/Documents/FISE A2/UE_E_Raug/file_example_WAV_1MG.wav').resampled_to(
        samplerate) as f:
    audio = f.read(f.frames)


# Make a pretty interesting sounding guitar pedalboard:
board = Pedalboard([
    Compressor(threshold_db=-50, ratio=25),
    Gain(gain_db=30),
    Chorus(),
    LadderFilter(mode=LadderFilter.Mode.HPF12, cutoff_hz=900),
    Phaser(),
    #Convolution("./guitar_amp.wav", 1.0),
    Reverb(room_size=0.25),
])

# Pedalboard objects behave like lists, so you can add plugins:
board.append(Compressor(threshold_db=-25, ratio=10))
board.append(Gain(gain_db=10))
board.append(Limiter())

# ... or change parameters easily:
board[0].threshold_db = -40

# Run the audio through this pedalboard!
effected = board(audio, samplerate)

# Write the audio back as a wav file:
with AudioFile('processed-output.wav', 'w', samplerate, effected.shape[0]) as f:
    f.write(effected)

#Crée un waveObject et le joue jusqu'à ce qu'il se termine
wave_obj = sa.WaveObject.from_wave_file('processed-output.wav')
play_obj = wave_obj.play()
#play_obj.wait_done()

board2= Pedalboard([LadderFilter(mode=LadderFilter.Mode.HPF12, cutoff_hz=900)])

rep = 0
print("change the cutoff value")

while play_obj.is_playing():
    rep = input()
    if rep !=0 :
        board2[0].cutoff_hz = rep
        effected2 = board2(audio, samplerate)

        # Write the audio back as a wav file:
        with AudioFile('processed-output.wav', 'w', samplerate, effected.shape[0]) as f:
            f.write(effected2)
            











