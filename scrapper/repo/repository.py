import sqlite3

from scrapper.entity.singleton import Singleton


class Repository(metaclass=Singleton):

    def __init__(self):
        self._connection = sqlite3.connect('../../cars.db', check_same_thread=False)
        self._connection.set_trace_callback(None)
        self._cursor = self._connection.cursor()


class GroupRepository(Repository):

    def __init__(self):
        super().__init__()
        self._cursor.execute('''
                CREATE TABLE IF NOT EXISTS subscribers(
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER NOT NULL UNIQUE
                )
                ''')
        self._connection.commit()

    def register_group_id(self, group_id: int):
        self._cursor.execute('''
        INSERT INTO subscribers (chat_id) VALUES (?)
        ''', (group_id,))
        self._connection.commit()

    def delete_group(self, group_id: int):
        self._cursor.execute('''
        DELETE FROM subscribers WHERE chat_id = ?
        ''', (group_id,))
        self._connection.commit()

    def is_already_subscribed(self, group_id: int) -> bool:
        self._cursor.execute('''
        SELECT EXISTS(SELECT chat_id FROM subscribers WHERE chat_id = ?)
        ''', (group_id,))
        return not not self._cursor.fetchone()[0]

    def get_all_chats(self):
        self._cursor.execute('''
            SELECT id, chat_id FROM subscribers
        ''')
        return self._cursor.fetchall()

    def get_all_ids(self):
        self._cursor.execute('''
            SELECT chat_id
            FROM subscribers
        ''')
        return self._cursor.fetchall()


class CarRepository(Repository):

    def __init__(self):
        super().__init__()
        self._cursor.execute("""
               CREATE TABLE IF NOT EXISTS cars(
                   id          INTEGER PRIMARY KEY AUTOINCREMENT,
                   autoria_id  INTEGER     NOT NULL,
                   price       REAL    NOT NULL
               )""")
        self._connection.commit()

    def save_all(self, cars: list):
        self._cursor.executemany('INSERT INTO cars(autoria_id, price) VALUES(?, ?)',
                                 tuple(map(lambda car: [car.autoria_id, car.new_price], cars)))
        self._connection.commit()

    def exists_by_id(self, id: str) -> bool:
        self._cursor.execute('''
            SELECT EXISTS (SELECT id FROM cars WHERE id = ?)
        ''', (id,))
        return not not self._cursor.fetchone()[0]

    def get_price_difference(self, autoria_id, price):
        self._cursor.execute('''
        SELECT 
            price - ?
        FROM 
            cars
        WHERE 
            autoria_id = ? AND price != ?
        ''', (price, autoria_id, price))
        return self._cursor.fetchone()
