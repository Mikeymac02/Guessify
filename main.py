from dotenv import load_dotenv
import os
import spotipy
import random
import re
import time
from spotipy.oauth2 import SpotifyOAuth
from fuzzywuzzy import fuzz


load_dotenv()
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
redirect_uri = os.getenv('redirect_uri')
scope = "user-modify-playback-state,user-read-playback-state,user-read-currently-playing,streaming,playlist-read-private,user-top-read,user-read-email,user-read-private"
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=redirect_uri, scope=scope))

def has_latin_characters(text):
    return bool(re.search(r'[a-zA-Z]', text))



def play(deviceId, uriVal, amt: int):
    spotify.start_playback(device_id=deviceId, uris=[uriVal], position_ms=0)
    started = False
    for _ in range(20):  # up to ~4 seconds
        state = spotify.current_playback()
        if state and state['is_playing'] and state['progress_ms'] > 800:
            started = True
            break
        time.sleep(0.1)  # check every 200ms
    time.sleep(amt)

    # Pause playback
    spotify.pause_playback(device_id=deviceId)
    return None

def guess_with_play_option(deviceId, uriVal, duration, correct_answer, artist, guess, currentGuesses):
    while True:
        targetScore = 93
        if len(correct_answer) <= 4:
            targetScore = 88
        else:
            targetScore == 93
        if len(currentGuesses) != 0:
            print("🧠 Your guesses so far:")
            for i, prev in enumerate(currentGuesses, 1):
                print(f"  {i}. {prev}")
        user_input = input(f"\n🎧 Guess #"+str(guess)+": Type 'play' to listen: ").strip().lower()
        score = fuzz.ratio(user_input, correct_answer)
        playScore = fuzz.ratio(user_input, 'play')

        if playScore >= 85:
            play(deviceId, uriVal, duration)
        elif score >= targetScore:
            print(f"✅ Correct! The song was '{correct_answer}' by {artist}")
            return True, user_input
        else:
            return False, user_input

def spordleChoice():
    results = []
    all_tracks=[]
    choice = int(input("What would you like to play?\n1. Your top tracks\n2. Sorry, only 1 choice is supported right now\nChoice: "))

    if choice == 1:
        results = spotify.current_user_top_tracks(limit=50, time_range='medium_term')
        all_tracks = results['items']
        for offset in [50, 100, 150, 200]:
            next_page = spotify.current_user_top_tracks(limit=50, offset=offset, time_range='medium_term')
            all_tracks.extend(next_page['items'])  # only add the track list, not the whole response

    return all_tracks


def get_active_device_id():
    devices = spotify.devices()['devices']

    for device in devices:
        if device.get('is_active'):
            return device['id']

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    devices = spotify.devices()['devices']
    print(devices)
    if not devices:
        print("No active Spotify devices found. Start Spotify on a device and try again.")
        exit()

    device_id = get_active_device_id()

    tracks = spordleChoice()

    #tracks = result['items']
    tracks = [track for track in tracks if has_latin_characters(track['name'])]
    CorrectSongs = 0
    IncorrectSongs = 0
    finished_songs = []
    while len(tracks) > 0:
        song = random.choice(tracks)
        tracks.remove(song)
        finished_songs.append(song)
        song_name = song['name'].lower()
        song_name = re.sub(r'\(.*?\)', '', song_name)
        song_name = song_name.split('-')[0].strip()
        artist_name = song['artists'][0]['name']
        uri = song['uri']

        guesses = []

        durations = [1, 2, 4, 7, 11, 16]
        for i, duration in enumerate(durations):
            if i > 0:
                print(f"❌ Incorrect. Playing {duration} seconds now...")
                print(duration)
                play(device_id, uri, duration)
            correct, guess = guess_with_play_option(device_id, uri, duration, song_name, artist_name, (i + 1), guesses)
            guesses.append(guess)
            if correct:
                CorrectSongs += 1
                print("You've guessed "+str(CorrectSongs)+" songs correctly and "+str(IncorrectSongs)+" incorrectly")
                break
        else:
            print(f"❌ Incorrect... The song was '{song_name}' by {artist_name}")
            IncorrectSongs += 1
            print("You've guessed " + str(CorrectSongs) + " songs correctly and " + str(IncorrectSongs) + " incorrectly")



