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

        width = 0.35  
        ind = np.arange(len(song_ids))  # the label locations

        fig, ax = plt.subplots(figsize=(12, 6))
        rects1 = ax.bar(ind - width/2, avg_popularity, width, label='Average Popularity', color='skyblue')
        rects2 = ax.bar(ind + width/2, song_occurences, width, label='Song Occurrences', color='orange')

        ax.set_xlabel('Song ID')
        ax.set_ylabel('Scores')
        ax.set_title('Average Popularity and Song Occurrences for Each Song')
        ax.set_xticks(ind)
        ax.set_xticklabels(song_ids)
        ax.legend()

        plt.show()

    except Exception as e:
        print(f"Error creating histogram: {str(e)}")

create_histogram(cur, conn)
