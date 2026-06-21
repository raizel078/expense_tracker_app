import sqlite3

from polars.io import database


def create_connection():
    conn = sqlite3.connect('database.db')
    return conn
