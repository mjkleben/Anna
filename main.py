from gtts import gTTS  # Google text-to-speech
import speech_recognition as sr
import subprocess
import time 
import os, sys
import pyautogui

# Import all commands used for Voice assistant
from commands import *

# Import webdriver for music, videos, etc.
from webdriver import *

from light_commands import *

# Import YouTube functions
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "addons"))
from youtubefunctions import *

# Set up the Speech Recognition and Microphone
recognizer = sr.Recognizer()
# microphone = sr.Microphone()

# Get the list of microphones
devices = sr.Microphone.list_microphone_names()

def new_wake_instance(new_instance, prev_instance):
    global recognizer
    # New timestamp of wake word happened
    if(new_instance!=prev_instance):
        subprocess.Popen([NIRCMD_PATH, "setsysvolume", str(1*VOLUME_MULTIPLER)])
        print("New instance occured!")
        try:
            print("Listening for command..")
            with sr.Microphone() as source:
                recognizer.pause_threshold = 0.5
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=10)

                try:
                    print("Performing speech to text..")
                    command = recognizer.recognize_google(audio).lower()

                    print(command)
                    # Check if it is a valid command, if so then perform command
                    is_command(command)

                except Exception as e:
                    print(e)
        except:
            print("Timed out")

    subprocess.Popen([NIRCMD_PATH, "setsysvolume", current_volume])
    return new_instance


# Using the value of hash table, dispatch the corresponding action of that value
def dispatch_command(action, command):
    global driver 
    global full_screened, is_paused

    print("DISPLATCHED")
    print(action)

    print(command)

    if(action=="lights"):
        toggle_lights()
    if(action=="youtube"):
        open_youtube_vid(command, driver, full_screened)

    if(action=="full screen"):
        full_screened = full_screen(driver, full_screened)
    if(action=="minimize screen"):
        full_screened = minimize_screen(driver, full_screened)
    if(action=="pause video"):
        print("Paused the video-------")
        is_paused = pause_video(driver, is_paused)
    if(action=="resume video"):
        print("Resumed the video-------")
        is_paused = resume_video(driver, is_paused)
    if(action=="volume"):
        print("Changing volume..")
        is_paused = change_volume(command)

# Determines whether the command is a valid command
# If valid then dispatch corresponding function to keyword
def is_command(command):
    print("IN COMMAND!")

    for keyword in all_commands.keys():
        if keyword in command:
            # Use if statements so it's a one time action then breaks
            # E.g. if a YouTube video has "turn off lights" we don't want to turn off the lights
            dispatch_command(all_commands[keyword], command)
        
    return False


def format_detection(process_id):
    wake_word_detector = subprocess.check_output(['docker', 'logs',  process_id], universal_newlines=True)
    detection_instance = wake_word_detector.split("\n")
    detection_instance = str(detection_instance[-2]).strip()
    return detection_instance


docker_image_id = "c7a8b75b121d"

# Loop to keep checking whether or not wake word has been said
prev_instance = format_detection(docker_image_id)

print("STARTING LOOP")

while True:
    new_instance = format_detection(docker_image_id)
    prev_instance = new_wake_instance(new_instance, prev_instance)