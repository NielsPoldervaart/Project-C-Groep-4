from flask import current_app
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, ForeignKey, Boolean, DECIMAL
from sqlalchemy.orm import mapper, sessionmaker, close_all_sessions
from sqlite_db_creation import create_connection_sqlite
"""
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
"""

db_location = "C:\\Users\\miame\\source\\repos\\Project-C-Groep-4\\server\\test_sqlite.db"
uri = "sqlite:///C:\\Users\\miame\\source\\repos\\Project-C-Groep-4\\server\\test_sqlite.db"
#SQLALCHEMY

#CLASSES, INIT DEFINED FOR OBJECT CREATION (NEEDED FOR INSERTING INTO DB)

class Gallery(object):
    def __init__(self, gallery_id, name):
        self.gallery_id = gallery_id
        self.name = name


class Company(object):
    def __init__(self, company_id, company_name, Gallery_gallery_id, Manual_manual_id):
        self.company_id = company_id
        self.company_name = company_name
        self.Gallery_gallery_id = Gallery_gallery_id
        self.Manual_manual_id = Manual_manual_id


class Role(object):
    def __init__(self, role_id, name):
        self.role_id = role_id
        self.name = name

class User(object):
    def __init__(self, user_id, username, email, password, verified, Company_company_id, Role_role_id):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.verified = verified
        self.Company_company_id = Company_company_id
        self.Role_role_id = Role_role_id

class Template(object):
    def __init__(self, template_id, template_file, Company_company_id):
        self.template_id = template_id
        self.template_file = template_file
        self.Company_company_id = Company_company_id

class Product(object):
    def __init__(self, product_id, product_file, price, verified, downloads, template_id, user_id, Gallery_gallery_id):
        self.product_id = product_id
        self.product_file = product_file
        self.price = price
        self.verified = verified
        self.downloads = downloads
        self.template_id = template_id
        self.user_id = user_id
        self.Gallery_gallery_id = Gallery_gallery_id

class Image(object):
    def __init__(self, image_id, image_path, Gallery_gallery_id):
        self.image_id = image_id
        self.image_path = image_path
        self.Gallery_gallery_id = Gallery_gallery_id

class Manual(object):
    def __init__(self, manual_id, manual_file):
        self.manual_id = manual_id
        self.manual_file = manual_file

#----------------------------------------------------------------------
#CREATES DATABASE STRUCTURE BY MAPPING ALL TABLE METADATA TO CORRECT ENGINE METADATA
def init_db_structure(database_URI):
    engine = create_engine(database_URI, echo=True)

    metadata = MetaData()

    gallery_table = Table(
        'Gallery', metadata, 
        Column('gallery_id', Integer, primary_key = True), 
        Column('name', String(length=255), nullable=False)
            )

    company_table = Table(
        'Company', metadata, 
        Column('company_id', Integer, primary_key = True), 
        Column('company_name', String(length=45), nullable=False), 
        Column('Gallery_gallery_id', Integer, ForeignKey("Gallery.gallery_id"), nullable=False),
        Column('Manual_manual_id', Integer, ForeignKey("Manual.manual_id"))
            )

    role_table = Table(
        'Role', metadata, 
        Column('role_id', Integer, primary_key = True), 
        Column('name', String(length=45), nullable=False)
            )

    user_table = Table(
        'User', metadata, 
        Column('user_id', Integer, primary_key = True), 
        Column('username', String(length=45), nullable=False),
        Column('email', String(length=255), nullable=False),
        Column('password', String(length=255), nullable=False),
        Column('verified', Boolean, nullable=False),
        Column('Company_company_id', Integer, ForeignKey("Company.company_id"), nullable=False),
        Column('Role_role_id', Integer, ForeignKey("Role.role_id"), nullable=False)
            )

    template_table = Table(
        'Template', metadata, 
        Column('template_id', Integer, primary_key = True), 
        Column('template_file', String(length=255), nullable=False),
        Column('Company_company_id', Integer, ForeignKey("Company.company_id"), nullable=False)
            )

    product_table = Table(
        'Product', metadata, 
        Column('product_id', Integer, primary_key = True), 
        Column('product_file', String(length=255), nullable=False),
        Column('price', DECIMAL(2,2), nullable=False), #TODO: CHECK WTF HAPPENS HERE
        Column('verified', Boolean, nullable=False),
        Column('downloads', Integer, nullable=False), 
        Column('template_id', Integer, ForeignKey("Template.template_id"), nullable=False), 
        Column('Company_company_id', Integer, ForeignKey("Company.company_id"), nullable=False)
            )

    image_table = Table(
        'Image', metadata, 
        Column('image_id', Integer, primary_key = True), 
        Column('image_path', String(length=255), nullable=False),
        Column('Gallery_gallery_id', Integer, ForeignKey("Gallery.gallery_id"), nullable=False)
            )

    manual_table = Table(
        'Manual', metadata, 
        Column('manual_id', Integer, primary_key = True), 
        Column('manual_file', String(length=255), nullable=False)
            )


    metadata.create_all(engine)

    """
    table_gallery = Table('Gallery', metadata, autoload=True)
    table_company = Table('Company', metadata, autoload=True)
    table_role = Table('Role', metadata, autoload=True)
    table_user = Table('User', metadata, autoload=True)
    table_template = Table('Template', metadata, autoload=True)
    table_product = Table('Product', metadata, autoload=True)
    table_image = Table('Image', metadata, autoload=True)
    table_manual = Table('Manual', metadata, autoload=True)
    """

    mapper(Gallery, gallery_table)
    mapper(Company, company_table)
    mapper(Role, role_table)
    mapper(User, user_table)
    mapper(Template, template_table)
    mapper(Product, product_table)
    mapper(Image, image_table)
    mapper(Manual, manual_table)

    #return engine

def create_db_session(database_URI):   
    engine = create_engine(database_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def createSession():
    create_connection_sqlite(db_location)
    init_db_structure(uri)
    session = create_db_session(uri)
    new_gallery = Gallery(None, "test_gal")
    new_gallery2 = Gallery(None, "test_gal2")
    session.add(new_gallery)
    session.add(new_gallery2)
    session.flush()
    res = session.query(Gallery).all()
    print(res[0].gallery_id, res[0].name)
    print(res[1].gallery_id, res[1].name)

def close_current_sessions():
    close_all_sessions()

#createSession()