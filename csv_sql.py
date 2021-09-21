import csv
import sqlite3


conn = sqlite3.connect('backend/api_foodgram/db.sqlite3')
cur = conn.cursor()

i = 1
with open('data/ingredients.csv', 'r', encoding='utf-8') as file:
    for line in file:
        data_1 = [i]
        data_2 = line.strip().rsplit(',', 1)
        data = tuple(data_1 + data_2)
        cur.execute("INSERT INTO recipes_ingredient VALUES(?, ?, ?);", data)
        i += 1
conn.commit()

conn.close()
