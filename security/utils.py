from flask import g


def check_is_fully_authenticated():
    return g.user is not None


def check_has_check_role(*roles):
    roles = [arg.upper() for arg in roles]
    return g.user is not None and g.user.role.name in roles


def check_is_owner(entity):
    return g.user is not None and entity.owned_by == g.user.id


def check_is_owner_or_has_role(entity, *roles):
    if g.user is None:
        return False
    elif entity.owned_by == g.user.id:
        return True

    roles = [arg.upper() for arg in roles]

    return g.user.role.name in roles
