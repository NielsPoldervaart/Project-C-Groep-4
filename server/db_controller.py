from werkzeug.security import generate_password_hash
from database_connection import *


def create_db_structure():
    init_db_structure()

def setup_basic_db(): #Inserts basic values into a database (ONLY WORKS IF DATABASE IS EMPTY)
    init_db_structure()
    with create_db_session() as db_session:

        roles = db_session.query(Role).first()
        gallery = db_session.query(Gallery).first()
        companies = db_session.query(Company).first()
        users = db_session.query(User).first()

        if roles == None and gallery == None and companies == None and users == None:

            #Add roles
            Role_Kynda_Admin = Role(None, "KYNDA_ADMIN")
            Role_Company_Admin = Role(None, "COMPANY_ADMIN")
            Role_Company_Employee = Role(None, "COMPANY_EMPLOYEE")
            db_session.add(Role_Kynda_Admin)
            db_session.add(Role_Company_Admin)
            db_session.add(Role_Company_Employee)
            #input()

            #Add gallery
            gallery = Gallery(None, "Kynda_gallery")
            db_session.add(gallery)
            
            #Add company
            company = Company(None, "Kynda", 1, None)
            db_session.add(company)

            #Add user
            user = User(None, "admin", generate_password_hash("admin@hr.nl"), generate_password_hash("KYNDA"), True, 1, 1)
            db_session.add(user)

            db_session.commit()
            db_session.close()


"""
def register_new_user(username, email, password, verified, company_id, role_id):
    with create_db_session() as db_session:
        db_session.add(User(None, username, generate_password_hash(email), generate_password_hash(password), verified, company_id, role_id))
        db_session.commit()


def login():
    pass
"""