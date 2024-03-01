from flask import Blueprint

bp = Blueprint('api_security', __name__)

from blueprints.api.security import routes
