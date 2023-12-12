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

def get_platforms_and_popularity(cur,conn):
    songs_dict={}
    cur.execute("SELECT artist_name,song_name,popularity,number_platforms FROM spotify_data JOIN song_ids ON spotify_data.song_id=song_ids.id JOIN songlink_data ON songlink_data.song_id=song_ids.id JOIN artist_ids ON spotify_data.artist_id=artist_ids.id GROUP BY song_name")
    info=cur.fetchall()
    for item in info:
        item_dict={}
        songs_dict[item[0]]=songs_dict.get(item[0],[])
        item_dict[item[1]]=item[2:4]
        songs_dict[item[0]].append(item_dict)

    artist_list=[]
    popularity_list=[]
    platform_list=[]
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
        artist_list.append(id)
        popularity_list.append(average_popularity)
        platform_list.append(average_platforms)
    return artist_list,popularity_list,platform_list

    
calculation=get_platforms_and_popularity(cur,conn)

def visualize_platforms_and_popularity(calculation):
    
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.scatter(calculation[1], calculation[0], c='blue', label='Scatterplot of Popularity')
    plt.title('Scatter Plot - Popularity by Artist')
    plt.xlabel('Popularity Score')
    plt.ylabel('Artist')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.scatter(calculation[2], calculation[0], c='red', label='Scatterplot of Platforms')
    plt.title('Scatter Plot - Platform Presence by Artist')
    plt.xlabel('Number of Platforms')
    plt.ylabel('Artist')
    plt.legend()

    plt.tight_layout()
    plt.show()

visualize_platforms_and_popularity(calculation)
