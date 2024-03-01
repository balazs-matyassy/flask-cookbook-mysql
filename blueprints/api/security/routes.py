from flask import session, request

from blueprints.api.security import bp
from security.api.decorators import is_fully_authenticated


@bp.route('/csrf_token')
@is_fully_authenticated
def get_csrf_token():
    return {
        'csrf_token': session.get('csrf_token'),
        '_links': {
            'self': request.path
        }
    }
