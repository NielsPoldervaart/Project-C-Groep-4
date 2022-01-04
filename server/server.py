from flask import Flask
from create_test_db_and_get_absolute_path import get_absolute_path

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

app.config["TEST_DATABASE_FILENAME"] = "test_sqlite.db"
#app.config["DATABASE_URI"] = "mysql+mysqldb://kynda:u9N3_HM+ARhDYsRQ@kynda-database.cgmcelrbhqyr.eu-west-2.rds.amazonaws.com/KyndaDB" #PROD DB CONNECTION
app.config["DATABASE_URI"] = "sqlite:///" + f"{get_absolute_path(app.config['TEST_DATABASE_FILENAME'])}" #TEST DB CONNECTION

if __name__ == "__main__":
    close_current_sessions()
    #create_all()
    init_db_structure()
    app.run(debug=True)