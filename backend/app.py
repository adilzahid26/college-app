from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room
from auth import auth_bp
from bio import bio_bp
from search import search_bp
from messages import messages_bp
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY') or 'secret_key'

# CORS for HTTP and WebSocket
CORS(app, supports_credentials=True, origins=["http://localhost:19006"])
socketio = SocketIO(app, cors_allowed_origins="*")  # <- upgraded from app.run

# Register HTTP routes
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(bio_bp)
app.register_blueprint(search_bp)
app.register_blueprint(messages_bp)

# --- Socket.IO Events ---
@socketio.on('join')
def on_join(data):
    user_id = data.get("user_id")
    if user_id:
        join_room(f"user_{user_id}")
        print(f"User {user_id} joined room user_{user_id}")

@socketio.on('send_message')
def on_send_message(data):
    sender_id = data.get("sender_id")
    receiver_id = data.get("receiver_id")
    content = data.get("content")
    
    # Insert into DB (just like your HTTP route)
    from messages.routes import insert_message
    insert_message(sender_id, receiver_id, content)

    # Emit message to receiver
    emit('receive_message', data, room=f"user_{receiver_id}")

# Run with socket support
if __name__ == "__main__":
    socketio.run(app, debug=True)
