"""Flask Application"""

# load libaries
from flask import Flask, jsonify
import sys

# load modules
from .blueprints.schemas_end import schema_end

# init Flask app
app = Flask(__name__)

# register blueprints. ensure that all paths are versioned!
app.register_blueprint(schema_end, url_prefix="/api/v1/schemas")