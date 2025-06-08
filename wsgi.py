import sys
import os
from dotenv import load_dotenv

# Update this with your actual project directory
project_home = '/home/sappasai/TAN_python_project'

# Add your project folder to the Python path
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load environment variables from .env file
load_dotenv(os.path.join(project_home, '.env'))

# Set the Flask app module
from app import app as application  # Assuming your Flask app is named app.py and app = Flask(__name__)
