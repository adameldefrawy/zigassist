import snowboydecoder
import sys
import signal
from gtts import gTTS
import speech_recognition as sr
import re
import webbrowser
import smtplib
import requests
from weather import Weather
import os

interrupted = False


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

model = sys.argv[1]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.6)
print('Listening... Press Ctrl+C to exit')


def talkToMe(audio):
    "speaks audio passed as argument"

    print(audio)
    for line in audio.splitlines():
    #  use the system's inbuilt say command instead of mpg123
      text_to_speech = gTTS(text=audio, lang='en')
      text_to_speech.save('audio.mp3')
      os.system('mpg123 audio.mp3')


def listen_for_command():
    detector.terminate()
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Listening...')
        snowboydecoder.play_audio_file()
        audio = r.record(source, duration=4)
        snowboydecoder.play_audio_file()
        print('Done Listening...')

    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
        if 'camera' in command:
            talkToMe('turning cameras on')
        if 'play' in command:
            os.system('mpg123 inmyfeelings.mp3')


    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard')


    detector.open_stream()
    detector.start(detected_callback=listen_for_command,
                    interrupt_check=interrupt_callback,
                    sleep_time=0.03)

# main loop
detector.start(detected_callback=listen_for_command,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
