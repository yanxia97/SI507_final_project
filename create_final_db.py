import csv
import json
import sqlite3 as sqlite

# Creates a database
def create_final_db():
    try:
        conn = sqlite.connect('yanxia_507_final.sqlite')
        cur = conn.cursor()
    except:
        print("fail!")
        return

    statement = '''
        DROP TABLE IF EXISTS 'Friends';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Games';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Players';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Game_Player';
    '''
    cur.execute(statement)
    conn.commit()
    
    statement = '''
        CREATE TABLE 'Friends' (
            'steamfriend1' INTEGER NOT NULL,
            'steamfriend2' INTEGER NOT NULL,
            'relationship' TEXT NOT NULL,
            'friend_since' TEXT
        );
    '''
    cur.execute(statement)
    statement = '''
        CREATE TABLE 'Games' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'AppId' INTEGER NOT NULL,
            'Name' TEXT NOT NULL
        );
    '''
    cur.execute(statement)
    statement = '''
        CREATE TABLE 'Players' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'SteamId' INTEGER NOT NULL,
            'Name' TEXT NOT NULL,
            'Url' TEXT NOT NULL,
            'TimeCreated' TEXT,
            'Country' TEXT,
            'State' TEXT,
            'City' TEXT
        );
    '''
    cur.execute(statement)
    statement = '''
        CREATE TABLE 'Game_Player' (
            'AppId' INTEGER NOT NULL,
            'OwnerId' INTEGER NOT NULL,
            'playtime_2weeks' INTEGER,
            'playtime_forever' INTEGER NOT NULL
        );
    '''
    cur.execute(statement)
    conn.commit()
    conn.close()


# Populates big10.sqlite database using csv files
def populate_final_db():

    try:
        conn = sqlite.connect('yanxia_507_final.sqlite')
        cur = conn.cursor()
    except:
        print("fail!")
        return

    with open('players.csv') as f:
        reader = csv.reader(f)
        rows = []
        for i,row in enumerate(reader):
            if (i>0 and row not in rows):
                rows.append(row)
                insertion = (None, row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                statement = 'INSERT INTO "Players" '
                statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
                cur.execute(statement, insertion)

    with open('games.json', 'r') as f:
        game_contents = f.read()
        GAME_DICTION = json.loads(game_contents)
        for key in GAME_DICTION:
            insertion = (None, int(key), GAME_DICTION[key])
            statement = 'INSERT INTO "Games" '
            statement += 'VALUES (?, ?, ?)'
            cur.execute(statement, insertion)

    with open('friends.csv') as f:
        reader = csv.reader(f)
        rows = []
        for i,row in enumerate(reader):
            if (i>0 and row not in rows):
                rows.append(row)
                statement = 'SELECT Id FROM Players WHERE SteamId = "'
                statement += row[0]
                statement += '"'
                cur.execute(statement)
                result = cur.fetchall()
                steamfriend1 = result[0][0]
                statement = 'SELECT Id FROM Players WHERE SteamId = "'
                statement += row[1]
                statement += '"'
                cur.execute(statement)
                result = cur.fetchall()
                steamfriend2 = result[0][0]
                insertion = (steamfriend1, steamfriend2, row[2], row[3])
                statement = 'INSERT INTO "Friends" '
                statement += 'VALUES (?, ?, ?, ?)'
                cur.execute(statement, insertion)

    with open('games.csv') as f:
        reader = csv.reader(f)
        rows = []
        for i,row in enumerate(reader):
            if (i>0 and row not in rows):
                rows.append(row)
                statement = 'SELECT Id FROM Games WHERE AppId = "'
                statement += row[0]
                statement += '"'
                cur.execute(statement)
                result = cur.fetchall()
                AppId = result[0][0]
                statement = 'SELECT Id FROM Players WHERE SteamId = "'
                statement += row[2]
                statement += '"'
                cur.execute(statement)
                result = cur.fetchall()
                OwnerId = result[0][0]
                insertion = (AppId, OwnerId, row[3], row[4])
                statement = 'INSERT INTO "Game_Player" '
                statement += 'VALUES (?, ?, ?, ?)'
                cur.execute(statement, insertion)

    # Close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_final_db()
    populate_final_db()
