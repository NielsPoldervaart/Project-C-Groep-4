from flask import request, session, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from user_verification import verify_user
from database_connection import *

init_api = Blueprint('init_api', __name__)

@init_api.route("/init/<datababase_URI>", methods=["GET"])
def login(database_URI):
    db_session = create_db_session(database_URI)

    if request.method == "GET":
        roles = db_session.query(Role).all()
        gallery = db_session.query(Gallery).all()
        companies = db_session.query(Company).all()
        users = db_session.query(User).all()

        if companies is None and users is None and roles is None and gallery is None:
            #Add roles
            Role_Kynda_Admin = Role(None, "KYNDA_ADMIN")
            Role_Company_Admin = Role(None, "COMPANY_ADMIN")
            Role_Company_Employee = Role(None, "COMPANY_EMPLOYEE")
            db_session.add(Role_Kynda_Admin, Role_Company_Admin, Role_Company_Employee)
            
            #Add gallery
            gallery = Gallery(None, "Kynda_gallery")
            db_session.add(gallery)

            #Add company
            company = Company(None, "Kynda", 1)
            db_session.add(company)

            #Add user
            user = User(None, "admin", generate_password_hash("admin@hr.nl"), generate_password_hash("KYNDA"), True)
            db_session.add(user)

            db_session.commit()
            return {}