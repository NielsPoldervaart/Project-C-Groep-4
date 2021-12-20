import pymysql

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker, close_all_sessions

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


#SQLALCHEMY

#CLASSES, INIT DEFINED FOR OBJECT CREATION (NEEDED FOR INSERTING INTO DB)
class Gallery(object):
    def __init__(self, gallery_id, name):
        self.gallery_id = gallery_id
        self.name = name

class Company(object):
    def __init__(self, company_id, company_name, Gallery_gallery_id):
        self.company_id = company_id
        self.company_name = company_name
        self.Gallery_gallery_id = Gallery_gallery_id


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

#----------------------------------------------------------------------
#CREATES DATABSE STRUCTURE BY MAPPING ALL TABLE METADATA TO CORRECT ENGINE METADATA
def init_db_structure():
    engine = create_engine('mysql+mysqldb://kynda:u9N3_HM+ARhDYsRQ@kynda-database.cgmcelrbhqyr.eu-west-2.rds.amazonaws.com/KyndaDB', echo=True)
    
    metadata = MetaData(engine)
    table_gallery = Table('Gallery', metadata, autoload=True)
    table_company = Table('Company', metadata, autoload=True)
    table_role = Table('Role', metadata, autoload=True)
    table_user = Table('User', metadata, autoload=True)
    table_template = Table('Template', metadata, autoload=True)
    table_product = Table('Product', metadata, autoload=True)
    table_image = Table('Image', metadata, autoload=True)

    mapper(Gallery, table_gallery)
    mapper(Company, table_company)
    mapper(Role, table_role)
    mapper(User, table_user)
    mapper(Template, table_template)
    mapper(Product, table_product)
    mapper(Image, table_image)

def create_db_session():   
    engine = create_engine('mysql+mysqldb://kynda:u9N3_HM+ARhDYsRQ@kynda-database.cgmcelrbhqyr.eu-west-2.rds.amazonaws.com/KyndaDB', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def createSession():
    init_db_structure()
    session = create_db_session()
    #templates = session.query(Template.template_id, Template.template_file, Company.company_id).join(Company).filter_by(company_id = f'{1}').all()
    #print(templates[0])
    #new_template = Template(None, 'test.html', 1)
    #session.add(new_template)
    #session.commit()
    #print("BREAK POINT\n\n\n\n\BREAKPOINT")
    res = session.query(Template).all()
    print(res[1].template_id, res[1].template_file)
    #res = session.query(User).filter_by(first_name='Hi').first()
    #testUser = User(2, "Yeet", "Teey", "Mail@mail.mail", "secure", 1, 1)
    #print(testUser.password)
    #print(res2[0].password)
    #print(type(res))
    #print(res == [])
    #print(res == None)
    #print(f"PASSWORD: {res[0].password}")
#createSession()

def close_current_sessions():
    close_all_sessions()