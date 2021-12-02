import pymysql

def db_connection():
    conn = None
    try:
        conn = pymysql.connect(
            host="sql11.freesqldatabase.com",
            database="sql11455878",
            user="sql11455878",
            password="tEwKz5RhgR",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.Error as e:
        print("\n\n\nERROR:", e)
    return conn