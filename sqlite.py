import sqlite3

# Connect to a new database file
connection = sqlite3.connect("imdb.db")
cursor = connection.cursor()

# Drop table if already exists (optional during testing)
cursor.execute("DROP TABLE IF EXISTS movies")

# Create the movies table
cursor.execute("""
CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    year INTEGER,
    genre TEXT,
    rating REAL,
    duration INTEGER,
    director TEXT
)
""")

# Insert 20 sample movie records
movies_data = [
    ("The Shawshank Redemption", 1994, "Drama", 9.3, 142, "Frank Darabont"),
    ("The Godfather", 1972, "Crime", 9.2, 175, "Francis Ford Coppola"),
    ("The Dark Knight", 2008, "Action", 9.0, 152, "Christopher Nolan"),
    ("Pulp Fiction", 1994, "Crime", 8.9, 154, "Quentin Tarantino"),
    ("Forrest Gump", 1994, "Drama", 8.8, 142, "Robert Zemeckis"),
    ("Inception", 2010, "Sci-Fi", 8.8, 148, "Christopher Nolan"),
    ("Fight Club", 1999, "Drama", 8.8, 139, "David Fincher"),
    ("The Matrix", 1999, "Sci-Fi", 8.7, 136, "The Wachowskis"),
    ("Goodfellas", 1990, "Crime", 8.7, 146, "Martin Scorsese"),
    ("The Silence of the Lambs", 1991, "Thriller", 8.6, 118, "Jonathan Demme"),
    ("Se7en", 1995, "Thriller", 8.6, 127, "David Fincher"),
    ("Interstellar", 2014, "Sci-Fi", 8.6, 169, "Christopher Nolan"),
    ("Parasite", 2019, "Thriller", 8.5, 132, "Bong Joon-ho"),
    ("The Green Mile", 1999, "Drama", 8.6, 189, "Frank Darabont"),
    ("The Prestige", 2006, "Mystery", 8.5, 130, "Christopher Nolan"),
    ("Whiplash", 2014, "Drama", 8.5, 107, "Damien Chazelle"),
    ("Gladiator", 2000, "Action", 8.5, 155, "Ridley Scott"),
    ("Joker", 2019, "Crime", 8.4, 122, "Todd Phillips"),
    ("The Departed", 2006, "Crime", 8.5, 151, "Martin Scorsese"),
    ("The Wolf of Wall Street", 2013, "Biography", 8.2, 180, "Martin Scorsese")
]

cursor.executemany("""
INSERT INTO movies (title, year, genre, rating, duration, director)
VALUES (?, ?, ?, ?, ?, ?)
""", movies_data)

# Fetch and display all rows to verify
print("Inserted IMDB-style movie records:\n")
rows = cursor.execute("SELECT * FROM movies").fetchall()
for row in rows:
    print(row)

# Commit and close connection
connection.commit()
connection.close()
