mport spotipy
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

def get_setlists_for_artists(api_key, artist):
    base_url = "https://api.setlist.fm/rest/1.0/search/setlists"
    headers = {
        'Accept': 'application/json',
        'x-api-key': 'E0Wf7sQUC93BOCSNEfplxwC9CXC9rQ84_CTh'
    }

    all_setlists = []

    params = {
        'artistName': artist
        }

    response = requests.get(base_url, params=params, headers=headers)

    if response.status_code == 200:
        setlists = response.json()['setlist']
        all_setlists.extend(setlists)
    else:
        print(f"Error getting setlists for {artist}: {response.content}")

    return all_setlists

def store_setlists_for_artists(data,track_list,cur,conn):

    song_count_dict={}

    cur.execute("CREATE TABLE IF NOT EXISTS setlist_song_data (artist_id INTEGER, song_id INTEGER, song_occurences INTEGER)")
    for item in data: 
        artist=item["artist"]["name"]
        try:
            query="SELECT id FROM artist_ids WHERE artist_name= ?" 
            cur.execute(query, (artist,))
            artist_id=cur.fetchone()
            artist_id=artist_id[0]
        except:
            continue
        all_sets=item["sets"]
        for set in all_sets:
            for song in all_sets["set"]:
                for item in song["song"]:
                    final_song=item["name"]  
                    song_count_dict[final_song]=song_count_dict.get(final_song,0)+1
        
    potential_track_list=track_list

    for track in potential_track_list: 
        song_title = track
        song_count= song_count_dict.get(song_title,0)
        query="SELECT id FROM song_ids WHERE song_name= ?"
        cur.execute(query, (song_title,))
        song_id=cur.fetchone()
        song_id=song_id[0]
        cur.execute("INSERT INTO setlist_song_data (artist_id,song_id, song_occurences) VALUES (?,?, ?)", (artist_id,song_id, song_count))
    conn.commit()
    return None

def store_tours_for_artists(data,cur,conn):
    limiter=0
    cur.execute("CREATE TABLE IF NOT EXISTS setlist_data (artist_id INTEGER, date TEXT, venue_id INTEGER)")
    for item in data:
        if limiter > 10:
            break
        else:
            try:
                artist=item["artist"]["name"]
                query="SELECT id FROM artist_ids WHERE artist_name= ?" 
                cur.execute(query, (artist,))
                artist_id=cur.fetchone()
                artist_id=artist_id[0]
                date=item["eventDate"]
                venue=item["venue"]["name"]
                query="SELECT id FROM venue_ids WHERE venue_name= ?" 
                cur.execute(query, (venue,))
                venue_id=cur.fetchone()
                venue_id=venue_id[0]
                cur.execute("INSERT INTO setlist_data (artist_id,date,venue_id) VALUES (?, ?,?)", (artist_id,date,venue_id))
                limiter+=1
            except:
                continue
    conn.commit()
    return None
