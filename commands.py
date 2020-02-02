# File holding all voice commands for assistant

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