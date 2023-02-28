# spotify_api

This repository id dedicated to learning the basics of working with API and JSON files.
There are two main python programs in total: first - artist_info.py and markets_map_app.py that both
work with Spotify API.


1. artist_info.py - main task of this program is to manipulate and navigate
through different parts of json file. Program takes input - artist's name, and returns
list of top 10 songs of the artist, album's year of release, album's name and, 
additionally, artist's id.

Examples of program at work:

<img width="989" alt="Screenshot 2023-02-28 at 03 19 53" src="https://user-images.githubusercontent.com/44242769/221727995-451d48ab-7590-473d-9c63-149a1d09269e.png">

<img width="974" alt="Screenshot 2023-02-28 at 03 20 25" src="https://user-images.githubusercontent.com/44242769/221728152-4909d9c0-cf73-4411-8d70-a2e7dcc82d7d.png">


2. markets_map_app.py - second program. It's essentially a web app (buit using Flask) that's
deployed on a pythonanywhere.com server. Link: https://aandrii.pythonanywhere.com. The program
recieves a name of an artist through the submit form on starting page. Once recieved, website
loads another page that contains a map of markers of all the countries(markets) where the most
popular song of that artist is available.

Example of program at work. Let's find the most popular song of a famous Swedish band ABBA and where 
this song is available to play on Spotify:

<img width="1655" alt="Screenshot 2023-02-28 at 21 43 42" src="https://user-images.githubusercontent.com/44242769/221962083-7b1a85a0-b71a-4c15-95a8-8349cb39cabc.png">



<img width="1655" alt="Screenshot 2023-02-28 at 21 44 09" src="https://user-images.githubusercontent.com/44242769/221962093-9b23a8da-3c63-453a-87aa-3b36f656a9fc.png">

Repository contains countries.csv file - it was created using both Nominatim and manually using Internet to speed up
the process of marking ALL locations from available_markets list.


