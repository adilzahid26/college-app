import os
import pymysql
from pymysql.cursors import DictCursor
from dotenv import load_dotenv
from flask import request, jsonify, Blueprint, session
from flask_cors import cross_origin

load_dotenv()
search_bp = Blueprint('search', __name__, url_prefix='/search')

def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        charset='utf8mb4',
        cursorclass=DictCursor
    )

@search_bp.route('', methods=['GET'])
@cross_origin(supports_credentials=True)
def search_users():
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, first_name, last_name, major, graduation_year, interests, hobbies
            FROM user
            WHERE id != %s
            ORDER BY last_name, first_name
        """, (user_id,))
        rows = cursor.fetchall()

        import json
        for row in rows:
            row['interests'] = json.loads(row['interests']) if row['interests'] else []
            row['hobbies'] = json.loads(row['hobbies']) if row['hobbies'] else []

        return jsonify(rows), 200
    finally:
        cursor.close()
        conn.close()
