# Guessify

Guessify is a command-line music guessing game powered by Spotify.  
It connects to your Spotify account, plays a few seconds of a song, and challenges you to guess the song title or artist before time runs out.

The project runs entirely in your local terminal — no web interface, no extra setup beyond Python and Spotify API credentials.

---

## Overview

Guessify uses the [Spotify Web API](https://developer.spotify.com) to pull tracks from your playlists and play snippets through your Spotify account.  
Because of this, you’ll need to set up a Spotify Developer account and create an application that provides an API key (Client ID and Client Secret).  
These credentials are stored locally in a `.env` file.

---

## Requirements

Before you start, make sure you have:

- **Python 3.8 or newer**, installed and added to PATH  
  (You can check by running `python --version` in Command Prompt.)
- A **Spotify Premium** account (Spotify only allows playback control for Premium users)
- A **Spotify Developer account** (free)
- **Git** (optional, but makes cloning easier)

---

## 0. Install Python
- If you do not have python installed, go to [Python Downloads](https://www.python.org/downloads/windows/)
    - Pick 'Download Windows installer (64-bit)' and run the installer
        - Reccomended to keep the default path so you don't have to change code
     
          
## 1. Set up Spotify Developer account

- Go to the [Spotify Developer Board](https://developer.spotify.com)
- Click the 'Log in' button in the top right and sign into your account
- Once signed in, click your username in the top right and then click the 'Dashboard' button
- Now in the dashboard, click the 'Create App' button
    - Give the app whatever name/description you want
    - Use the Redirect URI given in the .env.example file
    - Check off the Web API & Web Playback API
    - Click Save
- Once the app is created, you will see a new page that has your Client ID and a button that says 'View Client Secret'. Copy both keys down for later use

## 2. Clone the repository

Open Command Prompt and run (This will make a folder called "Guessify" in the current directory:

```cmd
git clone https://github.com/Mikeymac02/guessify.git
cd guessify
```

## 3. Set up .env file

- Copy/paste the .env.example file and call it .env
- Open the new file using notepad or another next editor
- Fill in the following values
  - Username: Your Spotify username (NOT YOUR EMAIL)
  - SPOTIFY_CLIENT_ID: The key copied from your API page
  - SPOTIFY_CLIENT_SECRET: The secret key copied from your API page
  - redirect_uri: http://127.9.9.1:8888/callback

## 4. Run the install.bat

- Follow the instructions on the command prompt once you double-click the install.bat

## 5. Run the game!

- Open a new command prompt
- cd into your guessify directory
- run 'py main.py' or 'python main.py depending on your python install



