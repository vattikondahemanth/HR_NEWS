from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'yourpassword',
    'database': 'yourdatabase',
    'cursorclass': pymysql.cursors.DictCursor
}

@app.route('/login', methods=['POST'])
def login():
    try:
        # Get data from request
        data = request.json
        username = data.get('username')
        password = data.get('password')

        # Validate input
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Connect to the database
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # SQL query to authenticate user
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()

        # Close the connection
        connection.close()

        if user:
            return jsonify({"message": "Login successful", "user": user}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
