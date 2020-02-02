# File for controlling lights for WiFi Power Switch
from volume import *

def toggle_lights():
    print("TURNED OFF LIGHTS")
    pyautogui.click(206, 186)