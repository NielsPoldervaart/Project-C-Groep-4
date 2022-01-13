from flask import request, session, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from user_verification import verify_user
from database_connection import *
from sqlite_db_creation import create_connection_sqlite

init_api = Blueprint('init_api', __name__)

@init_api.route("/init", methods=["GET"])
def login():
    #create_connection_sqlite(db_location)
    init_db_structure()
    db_session = create_db_session()

    if request.method == "GET":
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
        