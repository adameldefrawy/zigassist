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

def sendcommand(rigs, commandname):
    #array of rigs with master at index 0, rig number Y called by riglist[Y]
    riglist = ['192.168.50.133', '192.168.50.']

    #if not called on specific rig then called on master
    if not rigs:
        run_script = 'ssh pi@%s "python %s"' %(riglist[0], commandname)
        os.system(run_script)

    #called on specific rigs
    else
        for rig in rigs:
            run_script = 'ssh pi@%s "python3 8i/zig/scripts/zigcommand.py %s"' %(riglist[rig], commandname)
            os.system(run_script)


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

        # extract numbers if command asks for specific rigs
        command = replace_number_words(command)
        rigs = [int(s) for s in command.split() if s.isdigit()]
        if not rigs:
            #turn cameras off and on
            if 'turn' in command:
                if 'cameras' in command:
                    if 'on' in command:
                        talkToMe('turning cameras on')
                        sendcommand(rigs, 'pushpoweron')
                    elif 'off' in command:
                        talkToMe('turning cameras off')
                        sendcommand(rigs, 'pushpoweroff')

            #togglepower
            elif 'toggle' in command and 'power' in command:
                talkToMe('toggling power')
                sendcommand(rigs,'pushtogglepower')

            #storagemode on and off
            elif 'storage' in command and 'mode' in command:
                if 'on' in command:
                    talkToMe('pushing to storage mode')
                    sendcommand(rigs,'pushstoragemode')
                elif 'off' in command:
                    talkToMe('pushing to record mode')
                    #needtodothis

            #clear cards
            elif 'clear' in command and 'cards' in command:
                talkToMe('clearing cards')
                sendcommand(rigs,'pushclearcards')

            #clear pis
            elif 'clear' in command and 'pies' in command:
                talkToMe('clearing pi storage')
                sendcommand(rigs,'pushclearpistorage')

            #systemcheck
            elif 'system' in command and 'check' in command:
                talkToMe('executing system check')
                sendcommand(rigs,'systemcheck')


            #record
            elif 'record' in command:
                if 'start' in command:
                    talkToMe('Starting the recording')
                    sendcommand(rigs,'startrecord')
                elif 'stop' in command:
                    talkToMe('Stopping the recording')
                    sendcommand(rigs,'startrecord')

        else:
            if 'toggle' in command:
                sendcommand(rigs,'togglepower')

    #    if 'play' in command:
        #    os.system('mpg123 inmyfeelings.mp3')


    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard')

    detector.open_stream()
    detector.start(detected_callback=listen_for_command,
                    interrupt_check=interrupt_callback,
                    sleep_time=0.03)


def replace_number_words(word):
    string.replace(word, 'one', '1')
    string.replace(word, 'two', '2')
    string.replace(word, 'three', '3')
    string.replace(word, 'four', '4')
    string.replace(word, 'five', '5')
    string.replace(word, 'six', '6')
    string.replace(word, 'seven', '7')
    string.replace(word, 'eight', '8')
    string.replace(word, 'nine', '9')
    string.replace(word, 'ten', '10')
    return word

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

detector = snowboydecoder.HotwordDetector(models, sensitivity=.5)

print('Listening... Press Ctrl+C to exit')

# main loop
# make sure you have the same numbers of callbacks and models
detector.start(detected_callback=listen_for_command,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
