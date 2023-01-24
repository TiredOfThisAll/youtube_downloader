class Repository:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def create_schema(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS downloaded_music (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                url TEXT NOT NULL)
        """)

    def insert_downloaded_music(self, name, url):
        self.cursor.execute("""
            INSERT INTO downloaded_music (name, url)
            VALUES (?, ?)
        """, (name, url))

    def get_list_of_downloaded_music(self):
        return list(map(lambda x: x[0], self.cursor.execute("""
            SELECT id, name
            FROM downloaded_music
            ORDER BY id
        """).fetchall()))

    def delete_song_by_id(self, song_id):
        self.cursor.execute("""
            DELETE FROM downloaded_music
            WHERE id = ?
        """, (song_id,))

    def commit(self):
        self.connection.commit()
