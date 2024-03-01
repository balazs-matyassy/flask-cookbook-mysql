from flask import g, session

from persistence.repository.user import UserRepository


def init_app(app):
    app.before_request(__load_current_user)
    app.jinja_env.globals['is_fully_authenticated'] = lambda: g.user is not None
    app.jinja_env.globals['has_role'] = __has_role
    app.jinja_env.globals['is_owner'] = lambda entity: g.user is not None and entity.owned_by == g.user.id
    app.jinja_env.globals['is_owner_or_has_role'] = __is_owner_or_has_role
    app.jinja_env.globals['csrf_token'] = lambda: session['csrf_token']


def __load_current_user():
    if not session.get('user_id'):
        g.user = None
    else:
        g.user = UserRepository.find_by_id(session.get('user_id'))


def __has_role(*roles):
    return (g.user is not None
            and g.user.role.name in [role.upper() for role in roles])


def __is_owner_or_has_role(entity, *roles):
    return (g.user is not None
            and (entity.owned_by == g.user.id
                 or g.user.role.name in [role.upper() for role in roles]))
