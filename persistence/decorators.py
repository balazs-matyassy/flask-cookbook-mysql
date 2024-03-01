from datetime import datetime
import functools

from flask import g


def query(value):
    def query_decorator(view):
        @functools.wraps(view)
        def wrapped_view(cls, *args, **kwargs):
            with g.db.cursor() as cursor:
                if args:
                    cursor.execute(value, args)
                elif kwargs:
                    cursor.execute(value, kwargs)
                else:
                    cursor.execute(value)

                return view(cls, cursor)

        return wrapped_view

    return query_decorator


def fetchone(*join_keys):
    def fetchone_decorator(view):
        @functools.wraps(view)
        def wrapped_view(cls, cursor):
            return __create_entity(cls.get_entity_factory(), {}, cursor.fetchone())

        return wrapped_view

    def fetchone_join_decorator(view):
        @functools.wraps(view)
        def wrapped_view(cls, cursor):
            join_factories = {join_key: cls.get_join_factory(join_key) for join_key in join_keys}

            return __create_entity(cls.get_entity_factory(), join_factories, cursor.fetchone())

        return wrapped_view

    if len(join_keys) == 1 and callable(join_keys[0]):
        return fetchone_decorator(join_keys[0])
    elif not join_keys:
        return fetchone_decorator

    return fetchone_join_decorator


def fetchall(*join_keys):
    def fetchall_decorator(view):
        @functools.wraps(view)
        def wrapped_view(cls, cursor):
            return [__create_entity(cls.get_entity_factory(), {}, data) for data in cursor.fetchall()]

        return wrapped_view

    def fetchall_join_decorator(view):
        @functools.wraps(view)
        def wrapped_view(cls, cursor):
            join_factories = {join_key: cls.get_join_factory(join_key) for join_key in join_keys}

            return [__create_entity(cls.get_entity_factory(), join_factories, data) for data in cursor.fetchall()]

        return wrapped_view

    if len(join_keys) == 1 and callable(join_keys[0]):
        return fetchall_decorator(join_keys[0])
    elif not join_keys:
        return fetchall_decorator

    return fetchall_join_decorator


def update_authoring(view):
    @functools.wraps(view)
    def wrapped_view(entity):
        now = datetime.utcnow()

        if not entity.id:
            if hasattr(entity, 'created_at'):
                entity.created_at = now

            if hasattr(entity, 'created_by'):
                entity.created_by = g.user.id

        if hasattr(entity, 'modified_at'):
            entity.modified_at = now

        if hasattr(entity, 'modified_by'):
            entity.modified_by = g.user.id

        return view(entity)

    return wrapped_view


def update_ownership(view):
    @functools.wraps(view)
    def wrapped_view(entity):
        if not entity.id and hasattr(entity, 'owned_by'):
            entity.owned_by = g.user.id

        return view(entity)

    return wrapped_view


def statement(value):
    def statement_decorator(view):
        @functools.wraps(view)
        def wrapped_view(*args, **kwargs):
            with g.db.cursor() as cursor:
                if args:
                    cursor.execute(value, args)
                elif kwargs:
                    cursor.execute(value, kwargs)
                else:
                    cursor.execute(value)

                g.db.commit()

        return wrapped_view

    return statement_decorator


def entity_statement(value):
    def entity_statement_decorator(view):
        @functools.wraps(view)
        def wrapped_view(entity):
            with g.db.cursor() as cursor:
                cursor.execute(value, entity.form)
                g.db.commit()

        return wrapped_view

    return entity_statement_decorator


def insert_statement(value):
    def insert_decorator(view):
        @functools.wraps(view)
        def wrapped_view(entity):
            if not entity.id:
                with g.db.cursor() as cursor:
                    cursor.execute(value, entity.form)
                    g.db.commit()
                    entity.id = cursor.lastrowid

                    return entity

            return view(entity)

        return wrapped_view

    return insert_decorator


def update_statement(value):
    def update_decorator(view):
        @functools.wraps(view)
        def wrapped_view(entity):
            if entity.id:
                with g.db.cursor() as cursor:
                    cursor.execute(value, entity.form)
                    g.db.commit()

                    return entity

            return view(entity)

        return wrapped_view

    return update_decorator


def __create_entity(entity_factory, join_factories, data):
    entity = entity_factory(data)

    for join_key in join_factories:
        join_prefix = f'{join_key}_'
        join_data = {key[len(join_prefix):]: data[key] for key in data if key.startswith(join_prefix)}
        join_factory = join_factories[join_key]
        child = join_factory(join_data)

        setattr(entity, join_key, child)

    return entity
