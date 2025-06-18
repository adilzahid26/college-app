from flask import Flask
from flask_cors import CORS
from auth import auth_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    # Debug mode ON, but reloader OFF to avoid silent crashes
    app.run(debug=True, use_reloader=False)