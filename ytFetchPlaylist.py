# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def fetchVideos(youtube, playlistId, pageToken=None):
    request = youtube.playlistItems().list(
        part="id",
        maxResults=10,
        playlistId=playlistId,
        pageToken=pageToken
    )
    return request.execute()


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"
    playlistId = "PLy3-VH7qrUZ5IVq_lISnoccVIYZCMvi-8"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    # request = youtube.channels().list(
    #     part="snippet,contentDetails,statistics",
    #     managedByMe=True,
    #     onBehalfOfContentOwner="YOUR_CONTENT_OWNER_ID"
    # )
    # response = request.execute()
    #
    # print(response)

    result = fetchVideos(youtube, playlistId)
    videos = result['items']
    print (result)
    if "nextPageToken" in result.keys():
        while True:
            result = fetchVideos(youtube, playlistId, result['nextPageToken'])
            videos.extend(result['items'])
            if "nextPageToken" not in result.keys():
                break

    print(videos)


if __name__ == "__main__":
    main()
