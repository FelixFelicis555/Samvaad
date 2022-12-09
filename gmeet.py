from asyncore import read
from cmath import e
import os
import pyaudio
import wave
import os
import pyautogui
import speech_recognition as sr
import random
import pyttsx3
from googletrans import Translator,constants
from gtts import gTTS
from playsound import playsound
from pygame import _sdl2,mixer

mixer.init(devicename='Null Output')

try:
    j=0
    empty = 0
    lines = ''
    if 'Null Output' not in _sdl2.get_audio_device_names():
        os.system('pactl load-module module-null-sink')
        mixer.close()
        mixer.init(devicename='Null Output')
    while True:
        
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = 4


        p = pyaudio.PyAudio()
        WAVE_OUTPUT_FILENAME = str(j)+".wav"
            
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("* recording")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        translator = Translator()
        f = open('./script.txt', 'a')

        try:
            filename = WAVE_OUTPUT_FILENAME
            r = sr.Recognizer()
            with sr.AudioFile(filename) as source:
          
                audio_data = r.record(source)
                print('source: ', source)
                print('audio data: ', audio_data)
                
                text = r.recognize_google(audio_data, show_all=True)
                print(type(text))
                if text!="" and text!=None and text!=[] and type(text)!=list:
                    text = text['alternative'][0]['transcript']
                    translation = translator.translate(text, dest="hi")
                    print(text)
                    f.write(translation.text+'\n')
                    lines = lines + '\n' + translation.text
                else:
                    print('-----No Audio------')
                    print(empty)
                    empty += 1

            if empty>0:
                print(lines)

                tts = gTTS(lines, lang='hi', slow='False')
                tts.save('temp.mp3')
                mixer.music.load('temp.mp3')
                mixer.music.play()

                empty = 0
                f.close()
                f = open('./script.txt', 'w')
                f.close
                lines = ''
            

            os.remove(WAVE_OUTPUT_FILENAME) 
            f.close()

            
        except Exception:
            print('inner')
            print(e)
            continue

        j+=1
except Exception:
    print('outer')
    print(e)

mixer.quit()


