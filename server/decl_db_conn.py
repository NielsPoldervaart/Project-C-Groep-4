from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, sessionmaker, close_all_sessions
from flask import current_app

#SQLALCHEMY
#CLASSES, INIT DEFINED FOR OBJECT CREATION (NEEDED FOR INSERTING INTO DB)

def create_db_engine(database_URI):
    engine = create_engine(database_URI, echo=True)
    return engine

#database_uri = current_app.config["DATABASE_URI"]
database_uri = "sqlite://"
engine = create_db_engine(database_uri)
Base = declarative_base(engine)

class Gallery(Base):
    __tablename__ = 'Gallery'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, gallery_id, name):
        self.gallery_id = gallery_id
        self.name = name

def load_session():
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def test():
    db_conn = load_session()
    gal = Gallery(None, "Testgal1")
    db_conn.add(gal)
    db_conn.flush()
    res = db_conn.query(Gallery).all()
    print(res)

test()