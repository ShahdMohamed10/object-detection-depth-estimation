import sys
import os

# Add the project directory to the Python path
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.append(path)

# Import the Flask app
from api import app as application

# This is the WSGI entry point that PythonAnywhere looks for
if __name__ == '__main__':
    application.run() 