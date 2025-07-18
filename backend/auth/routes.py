from flask import Blueprint, request, jsonify, session
import os
import MySQLdb
from dotenv import load_dotenv
from flask_cors import cross_origin

load_dotenv()
auth_bp = Blueprint('auth', __name__)

def get_db_connection():
    return MySQLdb.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
    )

@auth_bp.route('/register', methods=['POST'])
@cross_origin(supports_credentials=True)
def register():
    try:
        data = request.json
        firstName = data.get('firstName')
        lastName = data.get('lastName')
        email = data.get('email')
        password = data.get('password')

        conn = get_db_connection()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM user WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return jsonify({"message": "Email already exists"}), 401
        else:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
                (firstName, lastName, email, password)
            )
            conn.commit()
            cursor.close()
            conn.close()

            return jsonify({"message": "User created"})
    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        conn = get_db_connection()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM user WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and user['password'] == password:
            session['user_id'] = user['id']
            return jsonify({
                "message": "Login successful",
                "user": {
                    "id": user['id']
                }
            })
        elif user:
            return jsonify({"message": "Incorrect Password"}), 401
        else:
            return jsonify({"message": "Invalid email"}), 401
    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/logout', methods=['POST'])
@cross_origin(supports_credentials=True)
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})


@auth_bp.route('/current_user', methods=['GET'])
@cross_origin(supports_credentials=True)
def current_user():
    if 'user_id' in session:
        return jsonify({
            "user": {
                "id": session['user_id']
            }
        })
    else:
        return jsonify({"user": None}), 401
