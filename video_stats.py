import requests
import json

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "MrBeast"
MAX_RESULTS = 50

url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"

def get_playlist_id():

    try:

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        channel_items = data["items"][0]
        playlist_ID = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        return playlist_ID

    except requests.exceptions.RaiseException as e:
        raise e


def get_video_id_list(playlist_id):

    video_ids = []
    pageToken = None
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={MAX_RESULTS}&playlistId={playlist_id}&key={API_KEY}"

    try:

        while True:
            
            url = base_url

            if pageToken:
                url += f"&pageToken={pageToken}"

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for item in data.get('items', []):
                video_id = item["contentDetails"]["videoId"]
                video_ids.append(video_id)

            pageToken = data.get('nextPageToken')
            
            if not pageToken:
                break

        return video_ids

    except requests.exceptions.RaiseException as e:
        raise e


def _video_batch_list(video_id_list, batch_size):
    for video_id in range(0, len(video_id_list), batch_size):
        yield video_id_list[video_id : video_id + batch_size]

def extract_video_data(video_ids):
    extracted_data = []

    try:
        for batch in _video_batch_list(video_ids, MAX_RESULTS):
            video_ids_str = ",".join(batch)
            batch_url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}"

            response = requests.get(batch_url)
            response.raise_for_status()
            data = response.json()

            for item in data.get('items', []):
                video_id = item["id"]
                snippet = item["snippet"]
                contentDetails = item['contentDetails']
                statistics = item['statistics']
            
                video_data = {
                    "video_id": video_id,
                    "title": snippet['title'],
                    "publishedAt": snippet.get('publishedAt', None),
                    "duration": contentDetails['duration'],
                    "viewCount": statistics.get('viewCount', None),
                    "likeCount": statistics.get('likeCount', None),
                    "commentCount": statistics.get('commentCount', None)
                }

                extracted_data.append(video_data)

        return extracted_data

    except requests.exceptions.RequestException as e:
        raise e


if __name__ == "__main__":
    playlist_id = get_playlist_id()
    video_id_list = get_video_id_list(playlist_id) 
    extracted_data = extract_video_data(video_id_list)
    print(extracted_data)

