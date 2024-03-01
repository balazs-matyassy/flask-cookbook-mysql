from flask import Blueprint

bp = Blueprint('api_categories', __name__)

from blueprints.api.categories import routes
