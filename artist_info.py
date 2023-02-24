"""Module doctring for artist_info.py

This module works with Spotify API, retrieves data
and outputs desired information about artist according
to input.

https://github.com/Karl9Doniz/spotify_api
"""


import json
from dotenv import load_dotenv
import os
import base64
from requests import post, get

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    """
    Gets token for further work with API.
    """

    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth_header(token):
    """
    Gets header for authorization using previously
    retrieved token.
    """

    return {"Authorization": "Bearer " + token}


def search_for_artist(token, artist_name):
    """
    Function returns artist id from token and strists's name.
    """

    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1"

    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artists with this name exists...")
    return json_result[0]


def get_info_by_artist(token, artist_id):
    """
    Returns top 10 songs (and albums where they appear + year of release), 
    name of the artist, artist id. 
    """

    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


if __name__ == "__main__":
    token = get_token()
    name = input()
    result = search_for_artist(token, name)
    artist_id = result["id"]
    top_songs = get_info_by_artist(token, artist_id)

    print("Artist: " + name + f" (id:{artist_id})")

    for idx, song in enumerate(top_songs):
        print(f"{idx + 1}. {song['name']}")
        print(f"Album: '{song['album']['name']}'\
 ({song['album']['release_date'].split('-')[0]})")
        try:
            print(f"Available in: {song['available_markets']}\n")
        except KeyError:
            continue
