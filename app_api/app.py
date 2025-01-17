from flask import Flask, request, jsonify, render_template
import pymysql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'amma9999',
    'database': 'world',
    'cursorclass': pymysql.cursors.DictCursor
}

@app.route('/', methods=['GET'])
def first_page():
    return render_template("login.html")

@app.route('/home', methods=['GET'])
def home_page():
    return render_template("home.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
    try:
        if request.method == 'GET':
            return render_template("login.html")
    
        usermail = request.form.get('usermail')
        password = request.form.get('password')

        # Validate input
        if not usermail or not password:
            return jsonify({"error": "usermail and password are required"}), 400

        # Connect to the database
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # SQL query to authenticate user
            query = "SELECT * FROM users WHERE mail = %s AND password = %s"
            cursor.execute(query, (usermail, password))
            user = cursor.fetchone()
            
        # Close the connection
        connection.close()
        print(user)
        if user:
            return render_template('home.html', user=user)
        else:
            return jsonify({"error": "Invalid usermail or password"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
