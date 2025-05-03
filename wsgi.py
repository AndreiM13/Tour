import sys
import os
from run import app  # Import your Flask app from run.py

# Add the directory where run.py is located to the system path
sys.path.insert(0, '/home/AndreiM13/Tour')  # Adjust this to your actual path

# Use this line to define your application for PythonAnywhere
application = app
