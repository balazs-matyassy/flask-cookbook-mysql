from flask import Blueprint

bp = Blueprint('api_recipes', __name__)

from blueprints.api.recipes import routes
