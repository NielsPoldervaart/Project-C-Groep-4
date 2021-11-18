from flask import Flask, request, jsonify, session
import json
import pymysql
import os

app = Flask(__name__)
app.secret_key = "ToBeSecret"

def db_connection():
    conn = None
    try:
        conn = pymysql.connect(
            host="sql11.freesqldatabase.com",
            database="sql11449887",
            user="sql11449887",
            password="j8Rl1xpF4g",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.Error as e:
        print("\n\n\nERROR:", e)
    return conn

@app.route("/templates/<company_id>", methods=["GET", "POST"])
def templates(company_id):

    user_verification = verify_user_and_company(company_id, [1,2,3])
    if user_verification != "PASSED":
        return user_verification

    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET": #View ALL templates from a company
        sql = f"""Select T.template_id, T.template_file, C.company_name From Template T
                    join Company C
                        on T.company_company_id = C.company_id
                    where C.company_id = {company_id};
        """
        cursor.execute(sql)
        templates = [
            dict(
                template_id = row['template_id'],
              template_file = row['template_file'],
                company_name = row['company_name']
                )
                for row in cursor.fetchall()
        ]  
        if len(templates) is not 0:
            return jsonify(templates)
        else:
            return {"Data:": "None"}

    if request.method == "POST": #Add a template to DB
        #TODO: ACTUAL TEMPLATE NEEDS TO BE ADDED TO STORAGE

        new_template_path = request.form["template_path"]

        sql = """INSERT INTO `Template` (Template_id, Template_file, Company_company_id)
                    Values(default, %s, %s)
        """
        cursor = cursor.execute(sql, (new_template_path, company_id))
        conn.commit()
        return "Template added succesfully"

@app.route("/template/<company_id>/<template_id>", methods=["GET", "DELETE"])
def template(company_id, template_id):

    user_verification = verify_user_and_company(company_id, [1,2,3])
    if user_verification != "PASSED":
        return user_verification

    conn = db_connection()
    cursor = conn.cursor()
    if request.method == "GET": #View a specific template
        sql = f"""Select * From Template
                    where template_id = {template_id}
                    and
                        company_company_id = {company_id};               
        """
        cursor.execute(sql)
        result = cursor.fetchone()
        if result is not None:
            return jsonify(result)
        return {"Data:": "None"}


    if request.method == "Delete" : #Delete a specific template
        sql = f"""Select template_file from Template where template_id = {template_id} and company_company_id = {company_id}
        """
        #sql2 = f"""Delete from Template where template_id = {template_id} and company_company_id = {company_id}
        #"""
        cursor.execute(sql)
        result = cursor.fetchone()
        path = result.get("template_file")
        os.remove(path)
        #cursor.execute(sql2)
        #conn.commit()
        return "Deleted File succesfully"


@app.route("/company/<company_id>", methods=["GET"])
def company(company_id):

    user_verification = verify_user_and_company(company_id, [1,2,3])
    if user_verification != "PASSED":
        return user_verification

    #DATABASE QUERY
    if request.method == "GET":
        conn = db_connection()
        cursor = conn.cursor()
        sql = f"""SELECT Company_id, Company_name FROM `Company` WHERE Company_id = {company_id}"""
        cursor.execute(sql)
        result = cursor.fetchone()
        if result is not None:
            return jsonify(result)
        return {"errorCode": 404, "Message": "Company Does not exist"""}


@app.route("/login", methods=["POST"])
def login():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "POST": #haal wachwoord van server voor juiste user
        inserted_password = request.form["password"]
        inserted_user_email = request.form["email"]

        sql = f"""Select user_id, company_company_id, role_role_id from User where password = "{inserted_password}" and email = "{inserted_user_email}" """
        cursor.execute(sql)
        user = cursor.fetchone()

        if user: #IF USER OBJECT IS NOT NONE (COULD FIND CORRECT DATA IN DB)
            session["user_id"] = user["user_id"]
            session["company_company_id"] = user["company_company_id"]
            session["role_role_id"] = user["role_role_id"]
            return "Succesfully logged in"

        else:
           return "Wrong credentials"

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("company_company_id", None)
    return "user logged out"


def verify_user_and_company(company_id, accepted_roles):
    ##ALL ROLES:
    #1: KYNDA_ADMIN
    #2: COMPANY_ADMIN (Kynda's Client)
    #3: COMPANY_WORKER (Kynda's Client)

    #VERIFY IF USER IN SESSION (LOGGED IN)
    if "user_id" and "company_company_id" not in session:
        return {"errorCode" : 403, "Message" : "Login not authorized"}

    #VERIFY IF USER IN COMPANY
    company_company_id = session["company_company_id"]
    if int(company_company_id) != int(company_id):
        return {"errorCode" : 403, "Message" : "Company not within User's companies"}

    #VERIFY IF USER HAS RIGHT ROLE
    role_role_id = session["role_role_id"]
    if int(role_role_id) not in accepted_roles:
        return {"errorCode" : 403, "Message" : "Required Role not within User's roles"}

    #PASSED ALL CHECKS
    return "PASSED"


if __name__ == "__main__":
    app.run(debug=True)