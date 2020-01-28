import subprocess
import os
import sys
import socket    

def start_detector_server():
    hostname = socket.gethostname()    
    IPAddr = socket.gethostbyname(hostname)  
    print(IPAddr) 
    docker_command = 'docker run -it -e PULSE_SERVER=' + str(IPAddr) + ' -e SNIPS_AUDIO_SERVER_ARGS="--alsa_capture=pulse --alsa_playback=pulse -v" -e SNIPS_AUDIO_SERVER_ENABLED="true" snips-pulseaudio-docker:latest'
    os.system(docker_command)


def get_server_id():
    docker_command = 'docker ps --filter "status=running" --format "{{.ID}}"'
    docker_id = subprocess.Popen(docker_command, stdout=subprocess.PIPE)
    return docker_id.communicate()[0].rstrip().decode('utf-8')

start_detector_server()
# print(get_server_id())
    





