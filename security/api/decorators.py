import functools

from flask import g, abort


def is_fully_authenticated(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            abort(401)

        return view(**kwargs)

    return wrapped_view


def has_role(*roles):
    roles = [arg.upper() for arg in roles]

    def has_role_decorator(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user is None or g.user.role.name not in roles:
                abort(401)

            return view(**kwargs)

        return wrapped_view

    return has_role_decorator


def is_owner(entity_name=None):
    def is_owner_decorator(view):
        @functools.wraps(view)
        def wrapped_view(*args, **kwargs):
            if g.user is None or kwargs[entity_name].owned_by != g.user.id:
                abort(401)

            return view(*args, **kwargs)

        return wrapped_view

    return is_owner_decorator


def is_owner_or_has_role(entity_name, *roles):
    roles = [arg.upper() for arg in roles]

    def is_owner_or_has_role_decorator(view):
        @functools.wraps(view)
        def wrapped_view(*args, **kwargs):
            if (g.user is None or
                    (kwargs[entity_name].owned_by != g.user.id and g.user.role.name not in roles)):
                abort(401)

            return view(*args, **kwargs)

        return wrapped_view

    return is_owner_or_has_role_decorator
