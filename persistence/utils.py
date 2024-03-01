from flask import g


def try_parse_int(value, default=None, lower=None, upper=None):
    try:
        result = int(value)

        if lower is not None and result < lower:
            result = lower
        elif upper is not None and result > upper:
            result = upper

        return result
    except ValueError:
        return default


def execute(query, args=None):
    with g.db.cursor() as cursor:
        cursor.execute(query, args)
        g.db.commit()

        return cursor.lastrowid


def fetchone(query, args=None):
    with g.db.cursor() as cursor:
        cursor.execute(query, args)

        return cursor.fetchone()


def fetchall(query, args=None):
    with g.db.cursor() as cursor:
        cursor.execute(query, args)

        return cursor.fetchall()
