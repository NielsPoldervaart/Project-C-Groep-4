import pymysql

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker

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

##SESSION TEST SQLALCHEMY
class Template(object):
    pass
#----------------------------------------------------------------------
def loadSession():
    """"""    
    engine = create_engine('mysql+mysqldb://sql11455878:tEwKz5RhgR@sql11.freesqldatabase.com/sql11455878', echo=True)
    
    metadata = MetaData(engine)
    moz_template = Table('Template', metadata, autoload=True)
    mapper(Template, moz_template)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def createSession():
    session = loadSession()
    res = session.query(Template).all()
    print(res[0].tamplate_file)

#createSession()