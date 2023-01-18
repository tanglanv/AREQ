import threading
import soundfile as sf
import numpy as np
import sounddevice as sd
import time
import scipy as sps
import pyloudnorm as pyln

class Sound:
    def __init__(self,path):
        print("init of sound")
        self.path = path
        self.gain = [0.5,0.5,0.5,0.5,0.5]
        self.loudness = [0.0,0.0,0.0,0.0,0.0]
        self.allLoudness = []




    def filter(self, data_eq, low_threshold_frequency, high_threshold_frequency):
        # Design the Butterworth filter
        nyquist = 0.5 * self.samplerate
        low = low_threshold_frequency / nyquist
        high = high_threshold_frequency / nyquist
        b, a = sps.signal.butter(4, [low, high], btype='band', analog=False, output='ba')

        # Apply the filter to the audio data using filtfilt
        filtered_audio_data = sps.signal.filtfilt(b, a, data_eq)
        return filtered_audio_data

    def _play(self):
        event = threading.Event()

        def callback(outdata, frames, time, status):
            # print("callback called")
            inputData = wf.buffer_read(frames, dtype='float32')
            # print("inputdata",len(inputData), " ", inputData[0:100])
            #print("inputData", len(inputData))
            dataArray = np.frombuffer(inputData, dtype='float32')

            # print("dataArray", type(dataArray),len(dataArray))




            filtered = []
            filtered.append(self.filter(dataArray, 120, 300))
            filtered.append(self.filter(dataArray, 300, 700))
            filtered.append(self.filter(dataArray, 700, 2600))
            filtered.append(self.filter(dataArray, 2600, 5200))
            filtered.append(self.filter(dataArray, 5200, 20000))

            #print("filtered", len(filtered)," ",len(filtered[0]) )

            amplified = [filtered[i] * self.gain[i] for i in range(len(filtered))]


            #print("amplified 0 : ",amplified[0])
            #print("filtered 0 : ",filtered[0])

            self.loudness = [self.get_loudness(data) for data in amplified]

            self.allLoudness.append(self.loudness)
            # print("loudness : ",self.loudness)

            recomposed = amplified[0] + amplified[1] + amplified[2] + amplified[3] + amplified[4]

            # print("recomposed : ", type(recomposed),len(recomposed))
            #print(" input: ", dataArray[20000:20100])

            recomposed = np.array(recomposed, dtype='float32')
            data = recomposed.tobytes()
            # print("data ",len(data), " ",data[0:100])

            if len(outdata) > len(data):
                outdata[:len(data)] = data
                outdata[len(data):] = b'\x00' * (len(outdata) - len(data))
                raise sd.CallbackStop
            else:
                outdata[:] = data
                # outdata = np.copy(data)

        with sf.SoundFile(self.path) as wf:
            self.samplerate = wf.samplerate
            stream = sd.RawOutputStream(samplerate=wf.samplerate,
                                        channels=wf.channels,
                                        callback=callback,
                                        blocksize=wf.samplerate,
                                        finished_callback=event.set)
            with stream:
                event.wait()

    def playsound(self):
        new_thread = threading.Thread(target=self._play)
        new_thread.start()

    def set_Gain(self,i,a):
        self.gain[i] = a

    def get_loudness(self,data):
        meter = pyln.Meter(self.samplerate)  # create BS.1770 meter
        loudness = meter.integrated_loudness(data)  # measure loudness
        return loudness




if __name__ == "__main__":
    sound = Sound("musique1.wav")
    sound.playsound()