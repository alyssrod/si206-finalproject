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
import matplotlib.pyplot as plt

conn = sqlite3.connect('final-database.db')
cur = conn.cursor()

def get_song_and_popularity(cur,conn):
    songs_dict={}
    cur.execute("SELECT song_name,popularity,song_occurences FROM spotify_data JOIN song_ids ON spotify_data.song_id=song_ids.id JOIN setlist_song_data ON setlist_song_data.song_id=song_ids.id JOIN artist_ids ON spotify_data.artist_id=artist_ids.id GROUP BY song_name")
    info=cur.fetchall()
    popularity_list=[]
    occurences=[]
    for item in info:
        popularity_list.append(item[1])
        occurences.append(item[2])
    return popularity_list,occurences

        

calculation=get_song_and_popularity(cur,conn)

def visualize_song_and_popularity(calculation):
    plt.figure(figsize=(10, 5))

    plt.scatter(calculation[0], calculation[1], c='blue', label='Scatterplot of Popularity')
    plt.title('Popularity and Setlists')
    plt.xlabel('Song Popularity Score')
    plt.ylabel('Occurences on Setlist')
    plt.legend()

    plt.tight_layout()
    plt.show()
visualize_song_and_popularity(calculation)
