from flask import request


def category_schema(category):
    return {
        'id': category.id,
        'name': category.name,
        'created_at': category.created_at,
        'modified_at': category.modified_at,
        '_links': {
            'self': request.path
        }
    }
