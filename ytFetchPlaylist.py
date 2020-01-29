#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import json
import logging
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

# import google_auth_oauthlib.flow
# import googleapiclient.discovery
# import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


# thanks https://github.com/googleapis/google-api-python-client/issues/325
# import hashlib
# import tempfile
#
# class DiscoveryCache:
#     def filename(self, url):
#         return os.path.join(os.getcwd(), 'google_api_discovery_' + hashlib.md5(url.encode()).hexdigest())
#
#     def get(self, url):
#         try:
#             with open(self.filename(url), 'rb') as f:
#                 return f.read().decode()
#         except FileNotFoundError:
#             return None
#
#     def set(self, url, content):
#         with tempfile.NamedTemporaryFile(delete=False) as f:
#             f.write(content.encode())
#             f.flush()
#             os.fsync(f)
#         os.rename(f.name, self.filename(url))


def fetch_videos(youtube, playlist_id, next_page_token=None):
    logging.debug("Fetching data from youtube...")
    request = youtube.playlistItems().list(
        part="id",
        maxResults=10,
        playlistId=playlist_id,
        pageToken=next_page_token
    )
    return request.execute()


def main(playlist_id):
    logging.info("Starting to fetch video ids from YouTube playlist: %s" % playlist_id)
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', scopes)
            # creds = flow.run_local_server(port=0)
            creds = flow.run_console()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)


    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"
    video_ids = []

    # Get credentials and create an API client
    # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    # credentials = flow.run_console()
    # youtube = build(api_service_name, api_version, credentials=creds, cache=DiscoveryCache())
    youtube = build(api_service_name, api_version, credentials=creds)

    # request = youtube.channels().list(
    #     part="snippet,contentDetails,statistics",
    #     managedByMe=True,
    #     onBehalfOfContentOwner="YOUR_CONTENT_OWNER_ID"
    # )
    # response = request.execute()
    #
    # print(response)

    result = fetch_videos(youtube, playlist_id)
    videos = result['items']
    print(result)
    if "nextPageToken" in result.keys():
        while True:
            result = fetch_videos(youtube, playlist_id, result['nextPageToken'])
            videos.extend(result['items'])
            if "nextPageToken" not in result.keys():
                break

    print(videos)
    for item in videos:
        if item['kind'] == "youtube#playlistItem":
            video_ids.append(item['id'])

    if len(video_ids):
        filename = "yt-playlist-video-ids-%s.json" % playlist_id
        with open(filename, 'w') as outfile:
            json.dump(video_ids, outfile)
        logging.info("Wrote %s video IDs to file %s" % (len(video_ids), filename))
    else:
        logging.warning("No video IDs found.")


if __name__ == "__main__":
    main("PLy3-VH7qrUZ5IVq_lISnoccVIYZCMvi-8")
