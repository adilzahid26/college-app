from flask import Blueprint, request, jsonify
import MySQLdb

auth_bp = Blueprint('auth', __name__)

def get_db_connection():
    return MySQLdb.connect(
        host='localhost',
        user='root',
        password='Az331684$',
        database='college_app',
    )

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        conn = get_db_connection()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM login WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and user['password'] == password:
            return jsonify({"message": "Login successful"})
        elif user and user['password'] != password:
            return jsonify({"message": "Incorrect Password"}), 401
        else:
            return jsonify({"message": "Invalid email"}), 401
    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500