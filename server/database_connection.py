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


#SQLALCHEMY

#CLASSES, INIT DEFINED FOR OBJECT CREATION (NEEDED FOR INSERTING INTO DB)
class Gallery(object):
    def __init__(self, gallery_id, name):
        self.gallery_id = gallery_id
        self.name = name

class Gallery_has_Company(object):
    def __init__(self, Company_company_id, Gallery_gallery_id):
        self.Company_company_id = Company_company_id
        self.Gallery_gallery_id = Gallery_gallery_id

class Collection(object):
    def __init__(self, collection_id, name, Gallery_gallery_id):
        self.collection_id = collection_id
        self.name = name
        self.Gallery_gallery_id = Gallery_gallery_id

class Company(object):
    def __init__(self, company_id, company_name, Collection_collection_id):
        self.company_id = company_id
        self.company_name = company_name
        self.Collection_collection_id = Collection_collection_id

class Role(object):
    def __init__(self, role_id, name):
        self.role_id = role_id
        self.name = name

class User(object):
    def __init__(self, user_id, first_name, last_name, email, password, Company_company_id, Role_role_id):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.Company_company_id = Company_company_id
        self.Role_role_id = Role_role_id

class Template(object):
    def __init__(self, template_id, template_file, Company_company_id):
        self.template_id = template_id
        self.template_file = template_file
        self.Company_company_id = Company_company_id

class Product(object):
    def __init__(self, product_id, price, verified, downloads, template_id, user_id, Gallery_gallery_id):
        self.product_id = product_id
        self.price = price
        self.verified = verified
        self.downloads = downloads
        self.template_id = template_id
        self.user_id = user_id
        self.Gallery_gallery_id = Gallery_gallery_id

class Image(object):
    def __init__(self, image_id, image_path):
        self.image_id = image_id
        self.image_path = image_path

class Image_has_Collection(object):
    def __init__(self, Image_image_id, Collection_collection_id):
        self.Image_image_id = Image_image_id
        self.Collection_collection_id = Collection_collection_id

#----------------------------------------------------------------------
#CREATES DATABSE STRUCTURE BY MAPPING ALL TABLE METADATA TO CORRECT ENGINE METADATA
def init_db_structure():
    engine = create_engine('mysql+mysqldb://kynda:u9N3_HM+ARhDYsRQ@kynda-database.cgmcelrbhqyr.eu-west-2.rds.amazonaws.com/KyndaDB', echo=True)
    
    metadata = MetaData(engine)
    table_gallery = Table('Gallery', metadata, autoload=True)
    table_Gallery_has_Company = Table('Gallery_has_Company', metadata, autoload=True)
    table_collection = Table('Collection', metadata, autoload=True)
    table_company = Table('Company', metadata, autoload=True)
    table_role = Table('Role', metadata, autoload=True)
    table_user = Table('User', metadata, autoload=True)
    table_template = Table('Template', metadata, autoload=True)
    table_product = Table('Product', metadata, autoload=True)
    table_image = Table('Image', metadata, autoload=True)
    table_image_has_collection = Table('Image_has_Collection', metadata, autoload=True)

    mapper(Gallery, table_gallery)
    #mapper(Gallery_has_Company, table_Gallery_has_Company)
    mapper(Collection, table_collection)
    mapper(Company, table_company)
    mapper(Role, table_role)
    mapper(User, table_user)
    mapper(Template, table_template)
    mapper(Product, table_product)
    mapper(Image, table_image)
    #mapper(Image_has_Collection, table_image_has_collection)

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