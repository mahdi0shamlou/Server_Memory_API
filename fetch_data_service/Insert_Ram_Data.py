import sqlite3
import time
from Get_Memory_Data import get_ram_info

def get_db_connection():
    conn = sqlite3.connect('../ram_data.db')
    conn.row_factory = sqlite3.Row
    return conn

def insert_ram_data():
    ram_info = get_ram_info()
    if ram_info:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ram (total, used, free) VALUES (?, ?, ?)
        ''', (ram_info['total'], ram_info['used'], ram_info['free']))
        conn.commit()
        conn.close()

if __name__ == '__main__':
    print('Start Get Ram data and save that data to db')
    while True:
        try:
            insert_ram_data()
            print('\tsaved data to db')

        except Exception as E:
            print(f'\tWe Get some Error -> {E}')

        finally:
            print('\tgo to sleep for 60 secend')
            time.sleep(60)