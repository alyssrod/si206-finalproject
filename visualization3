import matplotlib.pyplot as plt

def create_histogram(cur, conn):
    try:
        cur.execute("SELECT artist_id, AVG(popularity) FROM spotify_data GROUP BY artist_id")
        data = cur.fetchall()

        artist_ids, avg_popularity = zip(*data)

        artist_names = []
        for artist_id in artist_ids:
            cur.execute("SELECT artist_name FROM artist_ids WHERE id=?", (artist_id,))
            artist_name = cur.fetchone()[0]
            artist_names.append(artist_name)

        plt.figure(figsize=(10, 6))
        plt.bar(artist_names, avg_popularity, color='skyblue')
        plt.xlabel('Artist')
        plt.ylabel('Average Popularity')
        plt.title('Average Popularity of Songs by Artist')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        plt.show()

    except Exception as e:
        print(f"Error creating histogram: {str(e)}")

create_histogram(cur, conn)



