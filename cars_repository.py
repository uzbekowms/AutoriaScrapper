import sqlite3

connection = sqlite3.connect('cars.db')
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS cars(
    id          INT     AUTO INCREMENT,
    autoria_id  INT     NOT NULL,
    price       REAL    NOT NULL,
    PRIMARY KEY(id)
)""")
