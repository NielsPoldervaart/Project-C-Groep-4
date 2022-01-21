from flask import Flask
from create_test_db_and_get_absolute_path import get_absolute_path

from login_routes import login_api
from template_routes import template_api
from company_routes import company_api
from product_routes import product_api
from database_connection import init_db_structure, close_current_sessions
from image_routes import image_api
from init_routes import init_api
from generate_random_path import generate_random_path

app = Flask(__name__)
app.register_blueprint(login_api)
app.register_blueprint(template_api)
app.register_blueprint(product_api)
app.register_blueprint(company_api)
app.register_blueprint(image_api)
app.register_blueprint(init_api)
app.secret_key = generate_random_path(20, "") #Random string with 20 characters as secret key gets generated

app.config["TEST_DATABASE_FILENAME"] = "test_sqlite.db"
app.config["USING_TEST_FTP"] = False #UNCOMMENT WHEN USING TEST DB, TODO: change this to actual test config in flask for better modulation
app.config["DATABASE_URI"] = "mysql+mysqldb://kynda:u9N3_HM+ARhDYsRQ@kyndadb.cuny3kpvqmdq.eu-west-1.rds.amazonaws.com/KyndaDB" #PROD DB CONNECTION
# app.config["DATABASE_URI"] = "sqlite:///" + f"{get_absolute_path(app.config['TEST_DATABASE_FILENAME'])}" #TEST DB CONNECTION

if __name__ == "__main__":
    close_current_sessions()

    with app.app_context():
        init_db_structure()
        app.run(debug=True)