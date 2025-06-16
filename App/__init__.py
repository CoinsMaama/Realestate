from flask import Flask

# Create the Flask application instance
app = Flask(__name__)

# Package initialization
from .database import init_db
init_db()

# Import your routes if they're in separate files
# Uncomment these lines if you have route files:
# from . import routes
# from . import api
# etc.
