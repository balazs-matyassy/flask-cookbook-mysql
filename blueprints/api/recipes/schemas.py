from flask import url_for, request

from security.utils import check_is_owner_or_has_role


def recipe_schema(recipe):
    return {
        'id': recipe.id,
        'category_id': recipe.category.id,
        'name': recipe.name,
        'write_access': check_is_owner_or_has_role(recipe, 'ADMIN', 'MODERATOR'),
        'description': recipe.description,
        'difficulty': recipe.difficulty,
        'created_at': recipe.created_at,
        'modified_at': recipe.modified_at,
        '_links': {
            'self': request.path,
            'category': url_for('api_categories.get_category', category_id=recipe.category_id),
            'images': [
                url_for('recipes.download_image', recipe_id=recipe.id, image_id=image.id)
                for image
                in recipe.images
            ]
        }
    }
