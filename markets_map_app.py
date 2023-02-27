"""Module doctring for main.py

This module works with Spotify API, retrieves data
and outputs desired information about artist according
to input.

https://github.com/Karl9Doniz/spotify_api
"""


import json
import base64
import folium
from requests import post, get
from geopy.geocoders import Nominatim
import pycountry
from flask import Flask, render_template, request

# Flask app
app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        token = get_token()
        name = request.form["nm"]
        result = search_for_artist(token, name)
        artist_id = result["id"]
        top_songs = get_info_by_artist(token, artist_id)

        song = top_songs[0]
        id_song = song['id']
        countries = get_info_by_track(token, id_song)

        map_plot(countries)
        return render_template("markets_locations.html")
    else:
        return render_template("login.html")

CLIENT_ID="8aa6712d52d94dd68cec77e607aa9d89"
CLIENT_SECRET="dcc2d11a3c924a46b4e3bd58930891f9"

def get_token():
    """
    Gets token for further work with API.
    """

    auth_string = CLIENT_ID + ":" + CLIENT_SECRET
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
    Returns top 10 songs (and albums where they appear + year of release).
    """

    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


def get_info_by_track(token, song_id):
    """
    Returns info about a single track.
    """

    url = f"https://api.spotify.com/v1/tracks/{song_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["available_markets"]
    return json_result


def map_plot(countries):
    map = folium.Map(tiles="Stamen Terrain", zoom_start=10)
    fg = folium.FeatureGroup(name="Markets map")
    geolocator = Nominatim(user_agent="http")
    coords = []

    for market in countries[:20]:
        market_name = pycountry.countries.get(alpha_2=market).name
        location = geolocator.geocode(market_name)
        coords.append((location.latitude, location.longitude, market_name))

    for coord in coords:
        fg.add_child(folium.Marker(location=[coord[0], coord[1]], popup=coord[2], 
                                   icon=folium.Icon()))

    map.add_child(fg)
    map.save("spotify_api/templates/markets_locations.html")


if __name__ == "__main__":
    app.run()
