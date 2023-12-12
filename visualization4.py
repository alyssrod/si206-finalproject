import matplotlib.pyplot as plt
import numpy as np
import requests


def create_histogram(cur, conn):
    try:
        cur.execute("""
            SELECT s.song_id, AVG(popularity) AS avg_popularity, COALESCE(ssd.song_occurences, 0) AS song_occurences
            FROM spotify_data s
            LEFT JOIN setlist_song_data ssd ON s.song_id = ssd.song_id
            GROUP BY s.song_id
        """)
        data = cur.fetchall()

        song_ids, avg_popularity, song_occurences = zip(*data)

        bin_edges = np.arange(min(song_ids), max(song_ids) + 1, 1)

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.barh(bin_edges - 0.175, avg_popularity, height=0.35, label='Average Popularity', color='skyblue')
        ax.barh(bin_edges + 0.175, song_occurences, height=0.35, label='Song Occurrences', color='red')

        ax.set_ylabel('Song ID Range')
        ax.set_xlabel('Scores')
        ax.set_title('Average Popularity and Song Occurrences for Each Song')
        ax.set_yticks(bin_edges)
        ax.legend()

        plt.show()

    except Exception as e:
        print(f"Error creating histogram: {str(e)}")

create_histogram(cur, conn)

