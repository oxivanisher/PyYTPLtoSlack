#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import yaml
import logging
from googleapiclient.discovery import build

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def load_config():
    with open("yt_api_key.yaml", 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def fetch_videos(youtube, playlist_id, next_page_token=None):
    logging.debug("Fetching data from youtube...")
    request = youtube.playlistItems().list(
        part="snippet",
        maxResults=10,
        playlistId=playlist_id,
        pageToken=next_page_token
    )
    return request.execute()


def main(playlist_id):
    logging.info("Starting to fetch video ids from YouTube playlist: %s" % playlist_id)

    logging.debug("Loading API key")
    cfg = load_config()
    youtube = build("youtube", "v3", developerKey=cfg['yt_api_key'])

    result = fetch_videos(youtube, playlist_id)
    videos = result['items']
    if "nextPageToken" in result.keys():
        while True:
            result = fetch_videos(youtube, playlist_id, result['nextPageToken'])
            videos.extend(result['items'])
            if "nextPageToken" not in result.keys():
                break

    video_ids = []
    for item in videos:
        if item['kind'] == "youtube#playlistItem":
            video_ids.append(item['snippet']['resourceId']['videoId'])

    if len(video_ids):
        filename = "yt-playlist-video-ids-%s.json" % playlist_id
        with open(filename, 'w') as outfile:
            json.dump(video_ids, outfile)
        logging.info("Wrote %s video IDs to file %s" % (len(video_ids), filename))
    else:
        logging.warning("No video IDs found.")


if __name__ == "__main__":
    main(sys.argv[1])
