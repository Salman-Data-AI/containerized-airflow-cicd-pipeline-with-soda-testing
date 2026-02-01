import requests
import json

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "MrBeast"

url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"

def get_playlistid():

    try:

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        channel_items = data["items"][0]
        playlist_ID = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        print(playlist_ID)
        return playlist_ID

    except requests.exceptions.RaiseException as e:
        raise e

if __name__ == "__main__":
    get_playlistid()
    print("main gets executed")
else:
    print("main does not get executed")

