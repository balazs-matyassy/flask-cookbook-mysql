from flask import url_for

from blueprints.api.recipes import bp
from blueprints.api.recipes.schemas import recipe_schema
from blueprints.decorators import get_params, variable, entity_form, csrf_form, json_response
from persistence.model.recipe import Recipe
from persistence.repository.recipe import RecipeRepository
from security.api.decorators import has_role, is_owner_or_has_role


@bp.route('/')
@get_params('search')
@variable('recipes', RecipeRepository.find_all_by_name_like, 'search')
@variable('recipes', RecipeRepository.find_all)
@json_response(recipe_schema, 'recipes', collection=True)
def get_recipes(recipes):
    return recipes


@bp.route('/<int:recipe_id>')
@variable('recipe', RecipeRepository.find_by_id, 'recipe_id')
@json_response(recipe_schema, 'recipe')
def get_recipe(recipe):
    return recipe


@bp.route('/', methods=('POST',))
@has_role('ADMIN', 'MODERATOR', 'EDITOR')
@variable('recipe', Recipe)
@entity_form('form', 'recipe', csrf_validation=True, json=True, submit=True, repository=RecipeRepository)
@json_response(recipe_schema, 'form')
def create_recipe(form):
    if form.submitted_and_valid:
        return form, 201, url_for('api_recipes.get_recipe', recipe_id=form.entity.id)

    return form


@bp.route('/<int:recipe_id>', methods=('PUT',))
@variable('recipe', RecipeRepository.find_by_id, 'recipe_id')
@is_owner_or_has_role('recipe', 'ADMIN', 'MODERATOR')
@entity_form('form', 'recipe', csrf_validation=True, json=True, submit=True, repository=RecipeRepository)
@json_response(recipe_schema, 'form')
def update_recipe(form):
    return form


@bp.route('/<int:recipe_id>', methods=('DELETE',))
@variable('recipe', RecipeRepository.find_by_id, 'recipe_id')
@is_owner_or_has_role('recipe', 'ADMIN', 'MODERATOR')
@csrf_form('form', json=True, submit=True)
@json_response(None, 'recipe_id', 'form')
def delete_recipe(recipe_id, form):
    if not form.errors:
        try:
            RecipeRepository.delete_by_id(recipe_id)
            form.entity = 'Recipe.deleted.'
        except Exception as err:
            form.errors.append(str(err))

    return form
