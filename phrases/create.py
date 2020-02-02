from gtts import gTTS 
import os
from pygame import mixer  # Load the popular external library
mixer.init()


text = "I don't recognize that command"
language = 'en'
speech = gTTS(text = text, lang = language, slow = False)
speech.save('norecognize.mp3')


mixer.music.load('norecognize.mp3')
mixer.music.play()

input()