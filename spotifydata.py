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



client_id = '4c16a651c8e94c769cdf11ad1bb033a5'
client_secret = '2b5a3c867ff842b89a166674025eb7cc'

def get_spotify_token():
    
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = 'https://accounts.spotify.com/api/token'
    headers =  {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded'
    }  
    data = {'grant_type': 'client_credentials'}
    result = post(url, headers=headers, data=data)
    result_json = json.loads(result.content)
    token = result_json['access_token']
    return token 

def get_spotify_auth_header(token): 
    return {"Authorization": "Bearer " + token}

def spotify_artist_search(token, artist_name):

    url = "https://api.spotify.com/v1/search"
    headers = get_spotify_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1"
    query_url = url + '?' + query
    result = get(query_url, headers=headers)
    result_json = json.loads(result.content)['artists']['items']

    if len(result_json) == 0:
        print("No artist found with this name.")
        return None

    artist_info = result_json[0]
    
    return artist_info

def spotify_get_songs_by_artist(token, artist_id): 
    if not artist_id or 'id' not in artist_id:
        print("No artist found with this name.")
        return None

    artist_id = artist_id['id']
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_spotify_auth_header(token)
    result = {
        **get_spotify_auth_header(token),
        'Content-Type': 'application/json'
    }
    result = get(url, headers=headers)
    if result.status_code == 200:
        result_json = json.loads(result.content)["tracks"]
        return result_json
    
    else:
        print(f"Error getting top tracks: {result.content}")
        return None
    
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

cur, conn = setUpDatabase('final-database.db')
    
def store_spotify_data(track, cur, conn): 
    
    try: 
        cur.execute("CREATE TABLE IF NOT EXISTS spotify_data (song_id INTEGER, artist_id INTEGER, album TEXT, popularity INTEGER)")
        song_title = track['name']
        query="SELECT id FROM song_ids WHERE song_name= ?"
        cur.execute(query, (song_title,))
        song_id=cur.fetchone()
        song_id=song_id[0]
        artist = track['artists'][0]['name']
        query="SELECT id FROM artist_ids WHERE artist_name= ?"
        cur.execute(query, (artist,))
        artist_id=cur.fetchone()
        artist_id=artist_id[0]
        album = track['album']['name']
        popularity = track['popularity']
        cur.execute("INSERT INTO spotify_data (song_id, artist_id, album, popularity) VALUES (?, ?, ?, ?)", (song_id, artist_id, album, popularity))
        conn.commit()
        #print("Spotify data stored in the database successfully!")
    except Exception as e: 
        print(f"Error storing Spotify data: {str(e)}")


"""def create_final_database(cur, conn):
    cur.execute('''
              CREATE TABLE IF NOT EXISTS spotify_data (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  song_title TEXT,
                  artist TEXT,
                  album TEXT,
                  popularity INTEGER
              )
              ''')
    conn.commit()

    cur.execute('''
              CREATE TABLE IF NOT EXISTS artists (
                  id TEXT PRIMARY KEY,
                  name TEXT,
                  followers INTEGER,
                  popularity INTEGER
              )
              ''')
    conn.commit()

    cur.execute('''
              CREATE TABLE IF NOT EXISTS songs (
                  id TEXT PRIMARY KEY,
                  name TEXT,
                  artist_id TEXT,
                  FOREIGN KEY (artist_id) REFERENCES artists(id)
              )
              ''')
    conn.commit()

def insert_artist_info(artist_info, cur, conn):
    cur.execute('''
              INSERT OR REPLACE INTO artists (id, name, followers, popularity)
              VALUES (?, ?, ?, ?)
              ''', (artist_info['id'], artist_info['name'], artist_info['followers']['total'], artist_info['popularity']))

    conn.commit()
    print("Artist info stored in the database successfully!")

def insert_songs(songs, artist_id, cur, conn):
    cur, conn = setUpDatabase('final-database.db')
    cur.execute("SELECT id FROM artists WHERE id=?", (artist_id,))
    existing_artist = cur.fetchone()

    if existing_artist is None:
        print("Error: Artist not found in the artists table.")
        conn.close()
        return

    for song in songs:
        song_id = song['id']
        print("Inserting song:", song_id)

        cur.execute("SELECT id FROM songs WHERE id=?", (song_id,))
        existing_song = cur.fetchone()
        print("Existing Song:", existing_song)

        if existing_song is None:
            cur.execute('''
                        INSERT INTO songs (id, name, artist_id)
                        VALUES (?, ?, ?)
                        ''', (song_id, song['name'], artist_id))
            print("Song inserted:", song_id)
        else:
            print("Song already exists:", song_id)

    conn.commit()
    conn.close()

def store_spotify_data(track, cur, conn):
    song_title = track['name']
    artist = track['artists'][0]['name']
    album = track['album']['name']
    popularity = track['popularity']

    print(f"Storing Spotify data: {song_title}, {artist}, {album}, {popularity}")

    cur.execute("INSERT INTO spotify_data (song_title, artist, album, popularity) VALUES (?, ?, ?, ?)",
                (song_title, artist, album, popularity))
    conn.commit()
    print("Spotify data stored in the database successfully!")"""
