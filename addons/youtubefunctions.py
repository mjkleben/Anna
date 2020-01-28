import urllib
import re
import urllib.request



# Function for getting the YouTube url of a desired song
def get_youtube_url(desired_song):
    query_string = urllib.parse.urlencode({"search_query": desired_song})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    youtube_url = "http://www.youtube.com/watch?v=" + search_results[0]
    return youtube_url

def open_youtube_vid(desired_song, driver, is_fullscreened):
    driver.get(get_youtube_url(desired_song))
    if(is_fullscreened):
        full_screen_button = driver.find_element_by_class_name('ytp-fullscreen-button')
        full_screen_button.click()

def full_screen(driver, is_fullscreened):
    if(not is_fullscreened):
        full_screen_button = driver.find_element_by_class_name('ytp-fullscreen-button')
        full_screen_button.click()
        return True

def minimize_screen(driver, is_fullscreened):
    if(is_fullscreened):
        full_screen_button = driver.find_element_by_class_name('ytp-fullscreen-button')
        full_screen_button.click()
        return False

def pause_video(driver, is_paused):
    if(not is_paused):
        pause_button = driver.find_element_by_class_name('ytp-play-button')
        pause_button.click()
        return True


def resume_video(driver, is_paused):
    if(is_paused):
        play_button = driver.find_element_by_class_name('ytp-play-button')
        play_button.click()
        return False