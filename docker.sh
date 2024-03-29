#!/bin/bash
docker stop $(docker ps -aq)
echo y | docker system prune

# Start the pulseaudio.exe
C:\Users\Sang\Desktop\pulseaudio\bin
pulseaudio.exe --load="module-native-protocol-tcp auth-anonymous=1" --exit-idle-time=-1 --daemon


docker run -it -e PULSE_SERVER=192.168.0.199 -e SNIPS_AUDIO_SERVER_ARGS="--alsa_capture=pulse --alsa_playback=pulse -v" -e SNIPS_AUDIO_SERVER_ENABLED="true" snips-pulseaudio-docker:latest

