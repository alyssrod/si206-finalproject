import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import sqlite3
from requests import post, get 
import requests
import json
import base64
from bs4 import BeautifulSoup 
import requests
from spotifydata import get_spotify_token, spotify_artist_search, spotify_get_songs_by_artist

conn = sqlite3.connect('final-database.db')
cur = conn.cursor()

def get_songlink_data(song_url, title): 

    song_dict={}

    base="https://api.song.link/v1-alpha.1/links?url="
    link=song_url
    full_link=base+link

    response=requests.get(full_link)
    data=response.text
    data=json.loads(data)
    links=data["linksByPlatform"] 
    platforms=list(links.keys())

    song_dict[title]=(platforms,len(platforms))
    return(song_dict)

def store_songlink_data(data,cur,conn):
    
    cur.execute("CREATE TABLE IF NOT EXISTS songlink_data (song_id INTEGER, number_platforms INTEGER)")   
    for item in data:
        for key in item:
            title=key
            query="SELECT id FROM song_ids WHERE song_name= ?"
            cur.execute(query, (title,))
            song_id=cur.fetchone()
            song_id=song_id[0]
            number=item[key][1]
        cur.execute("INSERT INTO songlink_data (song_id,number_platforms) VALUES (?, ?)", (song_id, number))
    conn.commit()
    return None
