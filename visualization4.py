import matplotlib.pyplot as plt
import numpy as np

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
        rects1 = ax.hist(song_ids, bins=bin_edges - 0.175, weights=avg_popularity, width=0.35, label='Average Popularity', color='skyblue')
        rects2 = ax.hist(song_ids, bins=bin_edges + 0.175, weights=song_occurences, width=0.35, label='Song Occurrences', color='red')

        ax.set_xlabel('Song ID Range')
        ax.set_ylabel('Scores')
        ax.set_title('Average Popularity and Song Occurrences for Each Song')
        ax.set_xticks(bin_edges)
        ax.legend()

        plt.show()

    except Exception as e:
        print(f"Error creating histogram: {str(e)}")

create_histogram(cur, conn)
