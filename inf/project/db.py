import sqlite3

conn = sqlite3.connect("league.db")
cursor = conn.cursor()

# 1. League
cursor.execute("""
CREATE TABLE IF NOT EXISTS League (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
""")

# 2. Club
cursor.execute("""
CREATE TABLE IF NOT EXISTS Club (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    league_id INTEGER,
    name TEXT NOT NULL,
    table_place INTEGER,
    FOREIGN KEY (league_id) REFERENCES League(id)
);
""")

# 3. Club_stat
cursor.execute("""
CREATE TABLE IF NOT EXISTS Club_stat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    club_id INTEGER NOT NULL,
    win INTEGER NOT NULL DEFAULT 0,
    lose INTEGER NOT NULL DEFAULT 0,
    draw INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (club_id) REFERENCES Club(id)
);
""")

# 4. Match
cursor.execute("""
CREATE TABLE IF NOT EXISTS Match (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    club_id INTEGER NOT NULL,
    rival_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    score TEXT NOT NULL,
    FOREIGN KEY (club_id) REFERENCES Club(id),
    FOREIGN KEY (rival_id) REFERENCES Club(id)
);
""")

# 5. Player
cursor.execute("""
CREATE TABLE IF NOT EXISTS Player (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    club_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    salary INTEGER NOT NULL,
    FOREIGN KEY (club_id) REFERENCES Club(id)
);
""")

# 6. Player_stat
cursor.execute("""
CREATE TABLE IF NOT EXISTS Player_stat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    goals INTEGER NOT NULL DEFAULT 0,
    assists INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (player_id) REFERENCES Player(id)
);
""")

# 7. Coach
cursor.execute("""
CREATE TABLE IF NOT EXISTS Coach (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    club_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    salary INTEGER NOT NULL,
    FOREIGN KEY (club_id) REFERENCES Club(id)
);
""")

# 8. Coach_stat
cursor.execute("""
CREATE TABLE IF NOT EXISTS Coach_stat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    coach_id INTEGER NOT NULL,
    win INTEGER NOT NULL DEFAULT 0,
    lose INTEGER NOT NULL DEFAULT 0,
    draw INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (coach_id) REFERENCES Coach(id)
);
""")

# 9. Transfer
cursor.execute("""
CREATE TABLE IF NOT EXISTS Transfer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    club_from_id INTEGER NOT NULL,
    club_to_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    price INTEGER NOT NULL,
    FOREIGN KEY (player_id) REFERENCES Player(id),
    FOREIGN KEY (club_from_id) REFERENCES Club(id),
    FOREIGN KEY (club_to_id) REFERENCES Club(id)
);
""")

# 10. Contract
cursor.execute("""
CREATE TABLE IF NOT EXISTS Contract (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    player_id INTEGER NOT NULL, 
    club_id INTEGER NOT NULL, 
    date_start TEXT NOT NULL, 
    date_end TEXT NOT NULL,
    salary INTEGER NOT NULL,
    FOREIGN KEY (player_id) REFERENCES Player(id), 
    FOREIGN KEY (club_id) REFERENCES Club(id)
);
""")

conn.commit()
conn.close()

