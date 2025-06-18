App Set Up Guide

Verify Node.js, npm, Yarn, Python 3 are installed.
Open Terminal: 
Node.js: node -v, if not installed, go to nodejs.org
Npm: npm -v, comes with Node.js
Yarn: yarn -v, if not installed, first install Node.js and run “npm install -g yarn”
Python 3: python –version, if not installed, go to python.org
Set up frontend
Open Terminal:
Be in the right folder you want to make project in, use cd to change directory
Run “npx create-expo-app college-app” where npx is a tool that comes with npm, create-expo-app is use to create a new React Native project (React Native is used for mobile development), college-app is the name given to the folder
If it says “Need to install the following packages” enter y to proceed
Set up backend
Open Terminal:
Be in the project folder that frontend was set up in
Make directory for backend code “mkdir backend”
Change to that folder using “cd backend”
When creating a Python project, a virtual environment is needed to be setup. Run the command “python -m venv venv” where python is the interpreter that comes with Python 3, -m venv is used for creating virtual environments, the last venv is the name of the virtual environment
Open the environment with the command: “venv\Scripts\activate”
Install flask on this environment by running “pip install flask python-dotenv”, pip is the package installer for Python, flask is the name of the package, which is the framework to be used for this project, python-dotenv allows app to read environment variables from .env file
Install CORS so requests don’t get blocked when trying to fetch directly to Flask backend from Expo using command: “pip install flask-cors”.
NOTE: When the terminal is closed, virtual environment is closed, when new terminal is opened, just need to run command “venv\Scripts\activate”
Connecting backend with frontend
Create a file in backend folder in venv named app.py containing:
 
This allows the route /hello to have message passed in from backend flask side
Create .flaskenv file in backend folder containing:

This automatically tells flask that the entry point will be in app.py and the environment is development
Open 2 terminals side to side:
In the first one, make sure venv is running (venv) will be displayed at the beginning of the command line, then type “flask run”, this will start the Python App from the FLASK_APP entry point which is app.py.
In the second one, run “yarn start” or “npm start”, which will start the react app. The React Expo app will have some boiler plate code which can be filtered out by using “npm run reset-project”. In the terminal, there will be a link to go to localhost with the right port with the text “Web is waiting on”
In the entry point of the React side, index.tsx, add the following code:

This will fetch the api from backend and print the message, the first line from React side, the second from Flask side:

This is the basic endpoint connection from React to Flask using endpoint “Hello”

