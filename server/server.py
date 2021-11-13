from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

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

#Test API Route

@app.route("/gal", methods=["GET", "POST", "DELETE"])
def galleries():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor.execute("Select * FROM Gallery")
        galleries = [
            dict(
                gallery_id = row['gallery_id']
                )
                for row in cursor.fetchall()
        ]
        if galleries is not None:
            return jsonify(galleries)        
        else:
            return {"Data:": "None"}
    
    if request.method == "POST":
        sql = """
        INSERT INTO Gallery (gallery_id)
            Values(default)
        """
        cursor = cursor.execute(sql)
        conn.commit()
        return f"Gallery created successfully"

    if request.method == "DELETE":
        sql = """
        DELETE FROM Gallery
        """
        cursor = cursor.execute(sql)
        conn.commit()
        return f"All rows removed from Gallery"


@app.route("/templates/<company_id>", methods=["GET"])
def templates(company_id):
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        sql = f"""Select T.template_id, T.tamplate_file, C.company_name From Template T
                    join Company C
                        on T.company_company_id = C.company_id
                    where C.company_id = {company_id};
        """
        cursor.execute(sql)
    templates = [
        dict(
            template_id = row['template_id'],
            tamplate_file = row['tamplate_file'],
            company_name = row['company_name']
            )
            for row in cursor.fetchall()
    ]
    if len(templates) is not 0: #If list is not empty
        return jsonify(templates)
    else:
        return {"Data:": "None"}

@app.route("/template/<company_id>/<id>", methods=["GET"])
def template(company_id, id):
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET": ##TODO: Query something from Company as well ? (e.g Name for display)
        sql = f"""Select * From Template T
                    join Company C on 
                        C.company_id = T.company_company_id
                    where T.template_id = {id}
                    and
                        C.company_id = {company_id};
                        
        """
        cursor.execute(sql)
        result = cursor.fetchone()
        if result is not None:
            return jsonify(result)
        return {"Data:": "None"}

































if __name__ == "__main__":
    app.run(debug=True)