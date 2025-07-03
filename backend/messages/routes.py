import os
import pymysql
from pymysql.cursors import DictCursor
from dotenv import load_dotenv
from flask import request, jsonify, Blueprint, session
from flask_cors import cross_origin

load_dotenv()
messages_bp = Blueprint('messages', __name__, url_prefix='/messages')

def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        charset='utf8mb4',
        cursorclass=DictCursor
    )

@messages_bp.route('/<int:user_id>', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_messages(user_id):
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({'error': 'Not logged in'}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT * FROM messages
            WHERE (sender_id = %s AND receiver_id = %s)
               OR (sender_id = %s AND receiver_id = %s)
            ORDER BY timestamp
        """, (current_user_id, user_id, user_id, current_user_id))
        messages = cursor.fetchall()
        return jsonify(messages), 200
    finally:
        cursor.close()
        conn.close()

@messages_bp.route('', methods=['POST'])
@cross_origin(supports_credentials=True)
def send_message():
    data = request.get_json()
    current_user_id = session.get('user_id')
    receiver_id = data.get('receiver_id')
    content = data.get('content')

    if not current_user_id or not receiver_id or not content:
        return jsonify({'error': 'Invalid request'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # ✅ Manual check: make sure receiver exists
        cursor.execute("SELECT id FROM user WHERE id = %s", (receiver_id,))
        if cursor.fetchone() is None:
            return jsonify({'error': 'Receiver does not exist'}), 404

        # Optional: check if sender exists (usually not needed if session is safe)
        cursor.execute("SELECT id FROM user WHERE id = %s", (current_user_id,))
        if cursor.fetchone() is None:
            return jsonify({'error': 'Sender does not exist'}), 404

        cursor.execute("""
            INSERT INTO messages (sender_id, receiver_id, content)
            VALUES (%s, %s, %s)
        """, (current_user_id, receiver_id, content))
        conn.commit()
        return jsonify({'message': 'Sent'}), 201
    finally:
        cursor.close()
        conn.close()

def insert_message(sender_id, receiver_id, content):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO messages (sender_id, receiver_id, content)
            VALUES (%s, %s, %s)
        """, (sender_id, receiver_id, content))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
