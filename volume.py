# File for controlling volume on Windows machines
import os 
import subprocess

VOLUME_MULTIPLER = 6554 # Multiply this by a number 1-10
NIRCMD_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "driver", "nircmd.exe")
current_volume = str(8*VOLUME_MULTIPLER)
subprocess.Popen([NIRCMD_PATH, "setsysvolume", current_volume])

def change_volume(volume_command):
    global current_volume

    volume_numbers = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}
    for number in volume_numbers.keys():
        if number in volume_command:
            current_volume = str(volume_numbers[number]*VOLUME_MULTIPLER)

    print("CHANGED VOLUME")