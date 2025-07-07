import os
import pymysql
from pymysql.cursors import DictCursor
from dotenv import load_dotenv
from flask import request, jsonify, session, Blueprint
from flask_cors import cross_origin

load_dotenv()
bio_bp = Blueprint('bio', __name__, url_prefix='/bio')

def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        charset='utf8mb4',
        cursorclass=DictCursor 
    )

def get_current_user_id():
    return session.get('user_id')

@bio_bp.route('/<int:user_id>', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_bio(user_id):
    current_user_id = get_current_user_id()
    if not current_user_id or current_user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT first_name, last_name, major, graduation_year, interests, hobbies FROM user WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        if not row:
            return jsonify({}), 200

        import json
        row['interests'] = json.loads(row['interests']) if row['interests'] else []
        row['hobbies'] = json.loads(row['hobbies']) if row['hobbies'] else []

        return jsonify(row), 200
    finally:
        cursor.close()
        conn.close()

@bio_bp.route('', methods=['POST'])
@cross_origin(supports_credentials=True)
def save_bio():
    current_user_id = get_current_user_id()
    if not current_user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    user_id = data.get('id')
    if not user_id or user_id != current_user_id:
        return jsonify({"error": "Unauthorized"}), 401

    major = data.get('major', '')
    name = data.get('name')
    grad_year = data.get('gradYear')
    interests = data.get('interests', [])
    hobbies = data.get('hobbies', [])

    import json

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) AS count FROM user WHERE id = %s", (user_id,))
        exists = cursor.fetchone()['count'] > 0

        interests_json = json.dumps(interests)
        hobbies_json = json.dumps(hobbies)

        if exists:
            cursor.execute("""
                UPDATE user
                SET major = %s,
                    graduation_year = %s,
                    interests = %s,
                    hobbies = %s
                WHERE id = %s
            """, (major, grad_year, interests_json, hobbies_json, user_id))
        else:
            cursor.execute("""
                INSERT INTO user (id, first_name, major, graduation_year, interests, hobbies)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (user_id, name, major, grad_year, interests_json, hobbies_json))

        conn.commit()
        return jsonify({"message": "Bio saved successfully"}), 200
    finally:
        cursor.close()
        conn.close()
        
@bio_bp.route('/public/<int:user_id>', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_public_bio(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT first_name, last_name, major, graduation_year, interests, hobbies FROM user WHERE id = %s",
            (user_id,)
        )
        row = cursor.fetchone()
        if not row:
            return jsonify({"error": "User not found"}), 404

        import json
        row['interests'] = json.loads(row['interests']) if row['interests'] else []
        row['hobbies'] = json.loads(row['hobbies']) if row['hobbies'] else []

        return jsonify(row), 200
    finally:
        cursor.close()
        conn.close()