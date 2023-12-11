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
from setlistdata import *
from songlinkdata import *
from spotifydata import *

#sets up main id tables
cur, conn = setUpDatabase('final-database.db')
cur.execute("CREATE TABLE IF NOT EXISTS artist_ids(id INTEGER primary key, artist_name UNIQUE)")
cur.execute("CREATE TABLE IF NOT EXISTS song_ids(id INTEGER primary key, song_name UNIQUE)")
conn.commit()

#selects artist from a list and checks if already in artist id table 
artist_to_search=["Beyoncé", "Taylor Swift", "Hozier"]
for x in range(len(artist_to_search)):
    artist=artist_to_search[x] #add method to check if artist is in id table and continue if is
    cur.execute("SELECT artist_name FROM artist_ids")
    artist_list=cur.fetchall()
    current_artists=[]
    for item in artist_list:
        current_artists.append(item[0])
    if set(artist_to_search).issubset(current_artists):
        print("All artists updated!")
        exit()
    if artist not in current_artists:
        break
    else:
        continue 
        
#load lists for songlink and setlist and get top 10 songs from selected artist
songlink_urls=[]
songlink_titles=[]
spotify_track_list=[]

token = get_spotify_token()
artist_info = spotify_artist_search(token, artist)
if artist_info:
    songs = spotify_get_songs_by_artist(token, artist_info)
    if songs:
        for song in songs:
            songlink_input=(song["external_urls"]["spotify"])
            songlink_urls.append(songlink_input)
            spotify_track_list.append(song)
            songlink_titles.append(song["name"])
            song_artist=song['artists'][0]['name']
            cur.execute("INSERT OR IGNORE INTO artist_ids (artist_name) VALUES (?)", (song_artist,))
            conn.commit()
    else:
        print("No tracks found for this artist.")
else:
    print("No artist found with this name.")



#get all song ids from spotify top 10 list
def add_song_id_table(song,cur,conn):
    cur.execute("CREATE TABLE IF NOT EXISTS song_ids(id INTEGER primary key, song_name UNIQUE)")
    song_name=song
    cur.execute("INSERT OR IGNORE INTO song_ids (song_name) VALUES (?)", (song_name,))
    conn.commit()

#adds song to song id table
for item in spotify_track_list:
    add_song_id_table(item["name"], cur,conn)

#stores data for spotify tracks in table 
for song in spotify_track_list:
    store_spotify_data(song, cur, conn)

#stores songlink data
songlink_results=[]
index=0
for item in songlink_urls:
    title=songlink_titles[index]
    result=get_songlink_data(item,title)
    songlink_results.append(result)
    index+=1
store_songlink_data(songlink_results, cur, conn)

#stores both setlist tables
api_key = 'E0Wf7sQUC93BOCSNEfplxwC9CXC9rQ84_CTh'
artists_to_search = artist
result_setlists = get_setlists_for_artists(api_key, artists_to_search)
store_setlists_for_artists(result_setlists,cur,conn)
store_tours_for_artists(result_setlists,cur,conn)
