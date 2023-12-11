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
import matplotlib

conn = sqlite3.connect('final-database.db')
cur = conn.cursor()

def get_platforms_and_popularity(cur,conn):
    songs_dict={}
    cur.execute("SELECT artist_id,song_name,popularity,number_platforms FROM spotify_data JOIN song_ids ON spotify_data.song_id=song_ids.id JOIN songlink_data ON songlink_data.song_id=song_ids.id GROUP BY song_name")
    info=cur.fetchall()
    for item in info:
        item_dict={}
        songs_dict[item[0]]=songs_dict.get(item[0],[])
        item_dict[item[1]]=item[2:4]
        songs_dict[item[0]].append(item_dict)

    for id in songs_dict:
        average_popularity=0
        average_platforms=0
        total_songs=0
        for item in songs_dict[id]:
            for song in item:
                average_popularity+=item[song][0]
                average_platforms+=item[song][1]
                total_songs+=1
        average_popularity=average_popularity/total_songs
        average_platforms=average_platforms/total_songs
        return (id,average_popularity,average_platforms)

get_platforms_and_popularity(cur,conn)

def visualize_platforms_and_popularity():
    pass
