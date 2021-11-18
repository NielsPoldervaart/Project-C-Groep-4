from flask import Flask
from login_routes import login_api
from template_routes import template_api
from company_routes import company_api

app = Flask(__name__)
app.register_blueprint(login_api)
app.register_blueprint(template_api)
app.register_blueprint(company_api)
app.secret_key = "ToBeSecret" #TODO: Make Secret key actually secret

if __name__ == "__main__":
    app.run(debug=True)