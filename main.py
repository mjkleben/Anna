from gtts import gTTS  # Google text-to-speech
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import subprocess
import time 
import os, sys
import pyautogui


sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "addons"))
from youtubefunctions import open_youtube_vid, get_youtube_url, full_screen, minimize_screen, pause_video, resume_video

# Get file paths and set up the webdriver for controlling the browser
ADBLOCK_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "driver", "adblock.crx")
CHROME_DRIVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "driver", "chromedriver.exe")
# print(CHROME_DRIVER_PATH)
chrome_options = Options()
chrome_options.add_extension(ADBLOCK_PATH)
chrome_options.add_argument('start-maximized')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=CHROME_DRIVER_PATH)
print("SETTING DRIVER POSITION")
driver.set_window_position(-10000,-10000)
print("SWITCHING TABS")
driver.switch_to.window(driver.window_handles[0])

# VOLUME
VOLUME_MULTIPLER = 6554 # Multiply this by a number 1-10
NIRCMD_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "driver", "nircmd.exe")
current_volume = str(8*VOLUME_MULTIPLER)
subprocess.Popen([NIRCMD_PATH, "setsysvolume", current_volume])

#COMMANDS--------------------
# Initialize the commands
# Hash table with the keyword as a value so we can reduce overall runtime
all_commands = {}

def add_to_commands(function, keywords):
    for keyword in keywords:
        all_commands.update({keyword:function})

# Add the Youtube keywords to the hash table
youtube_commands = ['play', "listen to", "youtube"]
add_to_commands("youtube", youtube_commands)

volume_commands = ['volume']
add_to_commands("volume", volume_commands)

full_screened = False
full_screen_commands = ['full screen', 'maximize', 'screen bigger', 'fullscreen']
add_to_commands("full screen", full_screen_commands)
minimize_screen_commands = ['minimize', 'screen smaller']
add_to_commands("minimize screen", minimize_screen_commands)

# Commands to pause or resume video
is_paused = False
pause_video_commands = ['pause video', 'pause', 'stop the video']
add_to_commands("pause video", pause_video_commands)

resume_video_commands = ['resume video', 'continue']
add_to_commands("resume video", resume_video_commands)

light_commands = ['turn on lights', 'turn off lights', 'toggle lights']
add_to_commands("lights", light_commands)

camera_commands = ['turn on detector', 'bye', 'going out']
add_to_commands("camera", camera_commands)
#
#
#------------------------------

# Set up the Speech Recognition and Microphone
recognizer = sr.Recognizer()
# microphone = sr.Microphone()

# Get the list of microphones
devices = sr.Microphone.list_microphone_names()
# input(devices[1])


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


def change_volume(volume_command):
    global current_volume

    volume_numbers = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}
    for number in volume_numbers.keys():
        if number in volume_command:
            current_volume = str(volume_numbers[number]*VOLUME_MULTIPLER)

    print("CHANGED VOLUME")

def toggle_lights():
    print("TURNED OFF LIGHTS")
    pyautogui.click(206, 186)


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