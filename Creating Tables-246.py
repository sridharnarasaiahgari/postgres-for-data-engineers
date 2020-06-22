## 1. Incorrect Data Types ##

query_string = """
    INSERT INTO ign_reviews VALUES(
        5249979066121302000, 
        'Amazing', 
        'LittleBigPlanet PS Vita', 
        '/games/littlebigplanet-vita/vita-98907', 
        'PlayStation Vita', 
        9.0,
        'Platformer', 
        'Y', 
        2012, 
        9, 
        12
    );
"""
import psycopg2
conn = psycopg2.connect("dbname=dq user=dq")
cur = conn.cursor()
cur.execute(query_string)
conn.commit()
conn.close()

## 2. Describing a Table ##

import psycopg2
conn = psycopg2.connect("dbname = dq user = dq")
cur = conn.cursor()
cur.execute("SELECT * from ign_reviews LIMIT 0;")
conn.close()
print(cur.description)

## 3. Understanding the Description ##

import psycopg2
conn = psycopg2.connect("dbname=dq user=dq")
cur = conn.cursor()
cur.execute("SELECT typname FROM pg_catalog.pg_type WHERE oid = 25;")
type_name_25 = cur.fetchone()[0]
print(type_name_25)
cur.execute("SELECT typname FROM pg_catalog.pg_type WHERE oid = 700;")
type_name_700 = cur.fetchone()[0]
print(type_name_700)

## 4. Finding the Right id Data Type ##

import psycopg2
conn = psycopg2.connect("dbname=dq user=dq")
cur = conn.cursor()
cur.execute("alter table ign_reviews alter COLUMN id type bigint;")
conn.commit()
conn.close()

## 5. Float-like Types ##

import psycopg2
conn = psycopg2.connect("dbname=dq user=dq")
cur = conn.cursor()
cur.execute("ALTER TABLE ign_reviews ALTER COLUMN SCORE TYPE DECIMAL(3,1);")
conn.commit()
conn.close()

## 6. Finding the Max Length ##

import csv
with open('ign.csv', 'r') as f:
    next(f) # skip the row containing column headers
    reader = csv.reader(f)
    # create a set to contain all score phrases
    unique_words_in_score_phrase = set()
    for row in reader:
        # add the score phrase from this row to the set
        score_phrase = row[1]
        unique_words_in_score_phrase.add(score_phrase)
max_len = 0
for score_phrase in unique_words_in_score_phrase:
    max_len = max(max_len, len(score_phrase))
print(max_len)

## 7. Max String-like Datatypes ##

import psycopg2
conn = psycopg2.connect("dbname=dq user=dq")
cur = conn.cursor()
cur.execute("ALTER TABLE ign_reviews ALTER COLUMN score_phrase TYPE varchar(11);")
conn.commit()
conn.close()

## 8. Enumerated Datatypes ##

import psycopg2
conn = psycopg2.connect("dbname=dq user=dq")
cur = conn.cursor()
cur.execute("""
    CREATE TYPE evaluation_enum AS ENUM (
    'Great',       'Mediocre', 'Bad', 
    'Good',        'Awful',    'Okay', 
    'Masterpiece', 'Amazing',  'Unbearable', 
    'Disaster',    'Painful');
""")
# add your code below this comment
cur.execute("ALTER TABLE ign_reviews ALTER COLUMN score_phrase TYPE evaluation_enum USING score_phrase::evaluation_enum;")
conn.commit()
conn.close()

## 9. Understanding Enumerated Datatypes ##

import psycopg2
conn = psycopg2.connect("dbname=dq user=dq")
cur = conn.cursor()
cur.execute("""
    CREATE TYPE genre_enum AS ENUM (
    'Adventure', 'Strategy', 'Shooter', 'genre', 'Virtual Pet', 'Hardware', 'Adult', 'Baseball', 
    'Sports', 'Flight', 'Unknown', 'Racing', 'Battle', 'Fighting', 'Simulation', 'Party', 'Card', 
    'Productivity', 'Puzzle', 'Educational', 'Casino', 'RPG', 'Board', 'Other', 'Pinball', 'Platformer', 
    'Hunting', 'Action', 'Music', 'Compilation', 'Wrestling', 'Trivia');
""")
cur.execute("""
    CREATE TYPE platform_enum AS ENUM (
    'PC', 'Game Boy', 'Sega CD', 'Saturn', 'DVD / HD Video Game', 'Nintendo DSi', 
    'Arcade', 'Wii U', 'Lynx', 'Super NES', 'WonderSwan Color', 'TurboGrafx-CD', 
    'Windows Phone', 'TurboGrafx-16', 'N-Gage', 'Xbox One', 'Atari 2600', 
    'Pocket PC', 'Vectrex', 'Nintendo DS', 'Wireless', 'Ouya', 'Nintendo 64DD', 
    'Atari 5200', 'PlayStation 4', 'GameCube', 'Android', 'Wii', 'Game Boy Color', 
    'PlayStation 2', 'New Nintendo 3DS', 'Linux', 'Dreamcast VMU', 'Game Boy Advance', 
    'Windows Surface', 'Genesis', 'Xbox 360', 'Macintosh', 'Web Games', 'Nintendo 3DS', 'iPhone', 
    'SteamOS', 'Commodore 64/128', 'Dreamcast', 'PlayStation 3', 'NES', 'NeoGeo Pocket Color', 
    'Game.Com', 'PlayStation Portable', 'Master System', 'Sega 32X', 'NeoGeo', 'WonderSwan', 'iPad', 
    'Nintendo 64', 'PlayStation Vita', 'Xbox', 'iPod', 'PlayStation');
""")
# add your code below
cur.execute("ALTER TABLE ign_reviews ALTER COLUMN platform TYPE platform_enum USING platform::platform_enum;")

cur.execute("ALTER TABLE ign_reviews ALTER COLUMN genre TYPE genre_enum USING genre::genre_enum;")
cur.execute("ALTER TABLE ign_reviews ALTER COLUMN title TYPE varchar(200);")
cur.execute("ALTER TABLE ign_reviews ALTER COLUMN url TYPE varchar(200);")
conn.commit()
conn.close()

## 10. Boolean Types ##

import psycopg2
conn = psycopg2.connect("dbname=dq user=dq")
cur = conn.cursor()
cur.execute("""
    ALTER TABLE ign_reviews 
    ALTER COLUMN editors_choice TYPE boolean
    USING editors_choice::boolean;
""")
conn.commit()
conn.close()

## 11. Date Type ##

import psycopg2
conn = psycopg2.connect("dbname=dq user=dq")
cur = conn.cursor()
cur.execute("ALTER TABLE ign_reviews ADD COLUMN release_date date;")
cur.execute("ALTER TABLE ign_reviews DROP COLUMN release_year;")
cur.execute("ALTER TABLE ign_reviews DROP COLUMN release_month;")
cur.execute("ALTER TABLE ign_reviews DROP COLUMN release_day;")
conn.commit()
conn.close()

## 12. Loading the Data ##

import datetime
import psycopg2
import csv
conn = psycopg2.connect("dbname=dq user=dq")
cur = conn.cursor()
import csv
with open('ign.csv', 'r') as file:
    next(file) # skip csv header (first row with column titles)
    ign_data = csv.reader(file)
    for row in ign_data:
        # code to process and INSERT the row goes here
        year = int(row[8]) 
        month = int(row[9])
        day = int(row[10])
        date = datetime.date(year, month, day)
        row = row[:-3]
        row.append(date)
        cur.execute("INSERT INTO ign_reviews VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", row)
conn.commit()
conn.close()