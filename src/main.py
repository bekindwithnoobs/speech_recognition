from tkinter import *
from threading import Thread
from queue import Queue
import pyaudio
import subprocess
import json
from vosk import Model, KaldiRecognizer


CHANNELS = 1
FRAME_RATE = 16000
RECORD_SECONDS = 15
AUDIO_FORMAT = pyaudio.paInt16
SAMPLE_SIZE = 2
messages = Queue()
recordings = Queue()

def start_recording():
    messages.put(True)
    record = Thread(target = record_microphone)
    record.start()
    transcribe = Thread(target = speech_recognition)


def stop_recording():
    messages.get()

def record_microphone(chunk = 1024):
    p = pyaudio.PyAudio()
    stream = p.open(format = AUDIO_FORMAT,
                    channels = CHANNELS,
                    rate = FRAME_RATE,
                    input = True,
                    input_device_index = 1,
                    frames_per_buffer = chunk)
    frames = []
    while not messages.empty():
        data = stream.read(chunk)
        frames.append(data)
        if len(frames) >= (FRAME_RATE * RECORD_SECONDS) / chunk:
            recordings.put(frames.copy())
            frames = []
    
    stream.stop_stream()
    stream.close()
    p.terminate()

def speech_recognition(output):
    while not messages.empty():
        frames = recordings.get()
        rec.AcceptWaveform('b'.join(frames))
        result = rec.Result()
        text = json.loads(result)['text']
        print(text)

root = Tk() #root is window
root.geometry('300x300') #size of the window
l = Label(root, text="Start or stop the microphone")
l.pack()
b1 = Button(root, text= 'start recording', command=start_recording)
b1.pack()
b2 = Button(root, text= 'stop recording', command=stop_recording)
b2.pack()
root.mainloop()






model = Model(model_name = 'vosk-model-small-it-0.22')
rec = KaldiRecognizer(model, FRAME_RATE)
rec.SetWords(True)







