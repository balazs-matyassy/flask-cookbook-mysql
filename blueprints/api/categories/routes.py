from blueprints.api.categories import bp
from blueprints.api.categories.schemas import category_schema
from blueprints.decorators import get_params, variable, json_response
from persistence.repository.category import CategoryRepository


@bp.route('/')
@get_params('search')
@variable('categories', CategoryRepository.find_all_by_name_like, 'search')
@variable('categories', CategoryRepository.find_all)
@json_response(category_schema, 'categories', collection=True)
def get_categories(categories):
    return categories


@bp.route('/<int:category_id>')
@variable('category', CategoryRepository.find_by_id, 'category_id')
@json_response(category_schema, 'category')
def get_category(category):
    return category
