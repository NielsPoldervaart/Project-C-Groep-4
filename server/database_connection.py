import pymysql

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker

def db_connection():
    conn = None
    try:
        conn = pymysql.connect(
            host="kynda-database.cgmcelrbhqyr.eu-west-2.rds.amazonaws.com",
            database="KyndaDB",
            user="kynda",
            password="u9N3_HM+ARhDYsRQ",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.Error as e:
        print("\n\n\nERROR:", e)
    return conn


##SESSION TEST SQLALCHEMY
class Template(object):
    pass

class Company(object):
    pass

class User(object):
    pass
#----------------------------------------------------------------------
def loadSession():   
    engine = create_engine('mysql+mysqldb://kynda:u9N3_HM+ARhDYsRQ@kynda-database.cgmcelrbhqyr.eu-west-2.rds.amazonaws.com/KyndaDB', echo=True)
    
    metadata = MetaData(engine)
    table_template = Table('Template', metadata, autoload=True)
    table_company = Table('Company', metadata, autoload=True)
    table_user = Table('User', metadata, autoload=True)

    mapper(Template, table_template)
    mapper(Company, table_company)
    mapper(User, table_user)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def createSession():
    session = loadSession()
    res2 = session.query(User.first_name, User.password).all()
    res = session.query(User).filter_by(first_name='Hi').first()
    print(res2[0].password)
    print(type(res))
    print(res == [])
    print(res == None)
    #print(f"PASSWORD: {res[0].password}")

#createSession()