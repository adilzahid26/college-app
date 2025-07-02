from flask import Flask
from flask_cors import CORS
from auth import auth_bp
from bio import bio_bp
from search import search_bp
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY') or 'secret_key'

CORS(app, supports_credentials=True, origins=["http://localhost:19006"])

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(bio_bp) 
app.register_blueprint(search_bp) 

if __name__ == "__main__":
    app.run(debug=True)
