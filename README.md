# 8i Zig Assistant 


Zig Assistant is a voice assistant for use in testing of the Zig rig. It is to be installed into the console RaspberryPi in a 10-camera Zig Rig. The voice assistant can be used to turn the cameras on/off, start/stop recording, and push the rig to storage/record mode. The assistant responds to "ZigAssist" or "Adam". It can be further customized to integrate any potential Python or Shell scripts.

It employs the use of Google Text-To-Speech, Google Speech Recognition, and Snowboy Hotword Recognition.



## Setting Up

### Prerequisites
Run the following commands in the command line on the RaspberryPi to install all required dependencies and packages.

```
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get install python-pyaudio python3-pyaudio sox
$ sudo apt-get install portaudio19-dev
$ pip install pyaudio
$ pip install gTTs
$ pip install SpeechRecognition
$ sudo apt-get install swig
$ sudo apt-get install libatlas-base-dev
$ sudo apt-get install flac
$ sudo apt-get install mpg123
```

### Installing
Clone the zigassist repository into the home folder onto the RaspberryPi and set it up via the following commands.

```
$ git clone https://github.com/adameldefrawy/zigassist
$ cd zigassist/swig/Python3
$ make
```
### Setting up microphone and speakers

If using the <a href="http://wiki.seeedstudio.com/ReSpeaker_2_Mics_Pi_HAT/
">ReSpeaker 2 Mics Pi HAT</a>, plug it in (match the GPIO pins on the microphone to the Raspberry pi), give power via a micro-usb to the microphone, and run the following commands in the RaspberryPi:

```
$ git clone https://github.com/respeaker/seeed-voicecard.git
$ cd seeed-voicecard
$ sudo ./install.sh
$ sudo reboot
```

#### Changing Audio Settings on Pi
Enter the following in the Pi.

```
$ sudo alsamixer
```
If the 'card' setting in the top right does not match up with the microphone that is plugged in, the .asoundrc file needs to be adjusted.

* From the home directory:

	* `$ sudo nano .asoundrc`


	* Paste the following into the .asoundrc file

```
pcm.usb
{
	type hw
	card 1
}
pcm.internal
{
	type hw
	card ALSA
}
pcm.!default
{
	type asym
	playback.pcm
	{
    	type plug
    	slave.pcm "internal"
	}
	capture.pcm
	{
    	type plug
    	slave.pcm "usb"
	}
}
ctl.!default
{
	type asym
	playback.pcm
	{
    	type plug
    	slave.pcm "internal"
	}
	capture.pcm
	{
    	type plug
    	slave.pcm "usb"
	}
}
```


## Commands
**Commands for individual modules:**

* *"Toggle 1 2 ..."* -> Toggles power on whichever module numbers are specified

**Commands for master:**

* *"Turn cameras On* -> Turns all cameras on

* *"Turn cameras Off"* -> Turns all cameras off
* *"Toggle power"* -> Toggles power
* *"Storage mode on"*-> Puts Zig into storage mode
* *"Storage mode off"* -> Puts Zig into record mode
* *"System check"* -> Executes a system check to verify if settings are correct
* *"Start Record"* -> Starts a recording
* *"Stop Record"* -> Stops a recording
* For the following commands, a default recording time is written in the script. However, if a number is specified, it will record for that amount of seconds instead.
	 * *"Record Calibration (Optional Number)"* -> Records for 60 seconds (or specified number), stops recording, and stores the take as a calibration
	 * *"Record Clean Plate (Optional Number)"* -> Records for 10 seconds (or specified number), stops recording, and stores the take as a cleanplate
	* *"Record Normal (Optional Number)"* -> Records for 10 seconds (or specified number), stops recording, and stores the take as a normal take


## Adding Additional Commands

Additional commands can be added by modifying zigassist.py **listen_for_command** function.
