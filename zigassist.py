import snowboydecoder
import sys
import signal
from gtts import gTTS
import speech_recognition as sr
import re
import webbrowser
import smtplib
import requests
import os

interrupted = False

def talkToMe(audio):
    "speaks audio passed as argument"

    print(audio)
    for line in audio.splitlines():
    #  use the system's inbuilt say command instead of mpg123
      text_to_speech = gTTS(text=audio, lang='en')
      text_to_speech.save('audio.mp3')
      os.system('mpg123 audio.mp3')


#Listens for command once trigger word is heard
def listen_for_command():


    detector.terminate() #closes stream so that microphone can be used
    r = sr.Recognizer()

    #listens for four seconds in between beeps after wake word activated
    with sr.Microphone() as source:
        print('Listening...')
        snowboydecoder.play_audio_file()
        audio = r.record(source, duration=4)
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
        print('Done Listening...')

    # checks if four second audio clip has recognizable command
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
        if 'cameras' in command:
            if 'on' in command:
                talkToMe('turning cameras on')
            elif 'off' in command:
                talkToMe('turning cameras off')
        if 'togglepower' in command:
            talkToMe('toggling power')
        if 'storage' in command and 'mode' in command:
            if 'on' in command:
                talkToMe('pushing to storage mode')
            elif 'off' in command:
                talkToMe('pushing to record mode')
        if 'system' in command and 'check' in command:
            talkToMe('executing system check')
        if 'play' in command:
            os.system('mpg123 inmyfeelings.mp3')


    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard')

    detector.open_stream()
    detector.start(detected_callback=listen_for_command,
                    interrupt_check=interrupt_callback,
                    sleep_time=0.03)


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) != 3:
    print("Error: need to specify 2 model names")
    print("Usage: python demo.py 1st.model 2nd.model")
    sys.exit(-1)

models = sys.argv[1:]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

sensitivity = [0.5]*len(models)
detector = snowboydecoder.HotwordDetector(models, sensitivity=.5)
callbacks = [lambda: listen_for_command,
             lambda: listen_for_command]
print('Listening... Press Ctrl+C to exit')

# main loop
# make sure you have the same numbers of callbacks and models
detector.start(detected_callback=listen_for_command,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
