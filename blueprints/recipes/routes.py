from flask import flash, redirect, url_for

from blueprints.decorators import get_params, variable, html_response, \
    entity_form, csrf_form, http_response, file_response
from blueprints.recipes import bp
from persistence.model.image import Image
from persistence.model.ingredient import Ingredient
from persistence.model.recipe import Recipe
from persistence.repository.image import ImageRepository
from persistence.repository.ingredient import IngredientRepository
from persistence.repository.recipe import RecipeRepository
from security.decorators import has_role, is_owner_or_has_role


@bp.route('/')
@get_params('search')
@variable('recipes', RecipeRepository.find_all_by_name_like, 'search')
@variable('recipes', RecipeRepository.find_all)
@html_response('recipes/list.html', 'recipes')
def list_all(recipes):
    return recipes


@bp.route('/view/<int:recipe_id>')
@variable('recipe', RecipeRepository.find_by_id, 'recipe_id')
@html_response('recipes/view.html', 'recipe')
def view(recipe):
    return recipe


@bp.route('/create', methods=('GET', 'POST'))
@has_role('ADMIN', 'MODERATOR', 'EDITOR')
@variable('recipe', Recipe)
@entity_form('form', 'recipe', csrf_validation=True, submit=True, repository=RecipeRepository)
@html_response('recipes/form.html', 'form')
def create(form):
    if form.submitted_and_valid:
        flash('Recipe created.')

        return redirect(url_for('recipes.list_all'))

    return form


@bp.route('/edit/<int:recipe_id>', methods=('GET', 'POST'))
@variable('recipe', RecipeRepository.find_by_id, 'recipe_id')
@is_owner_or_has_role('recipe', 'ADMIN', 'MODERATOR')
@entity_form('form', 'recipe', csrf_validation=True, submit=True, repository=RecipeRepository)
@html_response('recipes/form.html', 'form', redirect_to='recipes_edit')
def edit(form):
    if form.submitted_and_valid:
        flash('Recipe saved.')

        return redirect(url_for('recipes.edit', recipe_id=form.entity.id))

    return form


@bp.route('/delete/<int:recipe_id>', methods=('POST',))
@variable('recipe', RecipeRepository.find_by_id, 'recipe_id')
@is_owner_or_has_role('recipe', 'ADMIN', 'MODERATOR')
@csrf_form('csrf', submit=True)
@http_response('recipe_id', 'csrf')
def delete(recipe_id, csrf):
    if csrf.errors:
        for error in csrf.errors:
            flash(error)
    else:
        try:
            RecipeRepository.delete_by_id(recipe_id)
            flash('Recipe deleted.')
        except Exception as err:
            flash(str(err))

    return redirect(url_for('recipes.list_all'))


@bp.route('/create-ingredient/<int:recipe_id>', methods=('GET', 'POST'))
@variable('recipe', RecipeRepository.find_by_id, 'recipe_id')
@is_owner_or_has_role('recipe', 'ADMIN', 'MODERATOR')
@variable('ingredient', Ingredient, 'recipe', dict_params=True)
@entity_form('form', 'ingredient', csrf_validation=True, submit=True, repository=IngredientRepository)
@html_response('recipes/ingredient_form.html', 'form')
def create_ingredient(form):
    if form.submitted_and_valid:
        flash('Ingredient created.')

        return redirect(url_for('recipes.create_ingredient', recipe_id=form.entity.recipe_id))

    return form


@bp.route('/edit-ingredient/<int:recipe_id>/<int:ingredient_id>', methods=('GET', 'POST'))
@variable('recipe', RecipeRepository.find_by_id, 'recipe_id')
@is_owner_or_has_role('recipe', 'ADMIN', 'MODERATOR')
@variable('ingredient', IngredientRepository.find_by_id_and_recipe_id, 'ingredient_id', 'recipe_id')
@entity_form('form', 'ingredient', csrf_validation=True, submit=True, repository=IngredientRepository)
@html_response('recipes/ingredient_form.html', 'form')
def edit_ingredient(form):
    if form.submitted_and_valid:
        flash('Ingredient saved.')

        return redirect(url_for(
            'recipes.edit_ingredient',
            recipe_id=form.entity.recipe_id,
            ingredient_id=form.entity.id
        ))

    return form


@bp.route('/delete-ingredient/<int:recipe_id>/<int:ingredient_id>', methods=('POST',))
@variable('recipe', RecipeRepository.find_by_id, 'recipe_id')
@is_owner_or_has_role('recipe', 'ADMIN', 'MODERATOR')
@variable('ingredient', IngredientRepository.find_by_id_and_recipe_id, 'ingredient_id', 'recipe_id')
@csrf_form('csrf', submit=True)
@get_params('redirect_to')
@http_response('recipe_id', 'ingredient_id', 'csrf', 'redirect_to')
def delete_ingredient(recipe_id, ingredient_id, csrf, redirect_to=None):
    if csrf.errors:
        for error in csrf.errors:
            flash(error)
    else:
        try:
            IngredientRepository.delete_by_id(ingredient_id)
            flash('Ingredient deleted.')
        except Exception as err:
            flash(str(err))

    if (redirect_to or '').lower() == 'recipes_edit':
        return redirect(url_for('recipes.edit', recipe_id=recipe_id))

    return redirect(url_for('recipes.create_ingredient', recipe_id=recipe_id))


@bp.route('/download-image/<int:recipe_id>/<int:image_id>')
@variable('recipe', RecipeRepository.find_by_id, 'recipe_id')
@variable('image', ImageRepository.find_by_id_and_recipe_id, 'image_id', 'recipe_id')
@file_response(True, 'image')
def download_image(image):
    return image


@bp.route('/upload-image/<int:recipe_id>', methods=('POST',))
@variable('recipe', RecipeRepository.find_by_id, 'recipe_id')
@is_owner_or_has_role('recipe', 'ADMIN', 'MODERATOR')
@variable('image', Image, 'recipe', dict_params=True)
@entity_form('form', 'image', csrf_validation=True, submit=True, repository=ImageRepository)
@http_response('form')
def upload_image(form):
    if form.submitted_and_valid:
        flash('Image uploaded.')
    elif form.errors:
        for error in form.errors:
            flash(error)

    return redirect(url_for('recipes.edit', recipe_id=form.entity.recipe_id))


@bp.route('/delete-image/<int:recipe_id>/<int:image_id>', methods=('POST',))
@variable('recipe', RecipeRepository.find_by_id, 'recipe_id')
@is_owner_or_has_role('recipe', 'ADMIN', 'MODERATOR')
@variable('image', ImageRepository.find_by_id_and_recipe_id, 'image_id', 'recipe_id')
@csrf_form('csrf', submit=True)
@http_response('recipe_id', 'image_id', 'csrf')
def delete_image(recipe_id, image_id, csrf):
    if csrf.errors:
        for error in csrf.errors:
            flash(error)
    else:
        try:
            ImageRepository.delete_by_id(image_id)
            flash('Image deleted.')
        except Exception as err:
            flash(str(err))

    return redirect(url_for('recipes.edit', recipe_id=recipe_id))
