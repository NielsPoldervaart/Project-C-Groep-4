import os
from sqlite_db_creation import create_connection_sqlite

def get_absolute_path(file): #CREATES TEST DB AND RETURNS PATH
    create_connection_sqlite(file)
    absolute_path = os.path.abspath(file)
    print(absolute_path)
    input()
    return absolute_path