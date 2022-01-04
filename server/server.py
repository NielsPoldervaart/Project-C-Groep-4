from flask import Flask
from login_routes import login_api
from template_routes import template_api
from company_routes import company_api
from product_routes import product_api
from database_connection import init_db_structure, close_current_sessions
from image_routes import image_api
from init_routes import init_api

app = Flask(__name__)
app.register_blueprint(login_api)
app.register_blueprint(template_api)
app.register_blueprint(product_api)
app.register_blueprint(company_api)
app.register_blueprint(image_api)
app.register_blueprint(init_api)
app.secret_key = "ToBeSecret" #TODO: Make Secret key actually secret

app.config["DATABASE_URI"] = "mysql+mysqldb://kynda:u9N3_HM+ARhDYsRQ@kynda-database.cgmcelrbhqyr.eu-west-2.rds.amazonaws.com/KyndaDB"
#app.config["DATABASE_URI"] = "sqlite:///C:\\Users\\miame\\source\\repos\\Project-C-Groep-4\\server\\test_sqlite.db"
if __name__ == "__main__":
    close_current_sessions()
    #create_all()
    init_db_structure(app.config["DATABASE_URI"])
    app.run(debug=True)