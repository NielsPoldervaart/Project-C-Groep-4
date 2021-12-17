from flask import session

def verify_user(company_id, accepted_roles=[1,2,3]):
    ##ALL ROLES:
    #1: KYNDA_ADMIN
    #2: COMPANY_ADMIN (Kynda's Client)
    #3: COMPANY_WORKER (Kynda's Client)

    #VERIFY IF USER IN SESSION (LOGGED IN)
    if "user_id" and "company_company_id" not in session:
        return {"errorCode" : 401, "Message" : "Login not authorized"}, 401

    #VERIFY IF USER IN COMPANY
    company_company_id = session["company_company_id"]
    if int(company_company_id) != int(company_id):
        return {"errorCode" : 403, "Message" : "Company not within User's companies"}, 403

    #VERIFY IF USER HAS RIGHT ROLE
    role_role_id = session["role_role_id"]
    if int(role_role_id) not in accepted_roles:
        return {"errorCode" : 403, "Message" : "Required Role not within User's roles"}, 403

    #PASSED ALL CHECKS
    return "PASSED"