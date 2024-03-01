
from flask import flash, redirect, url_for

from blueprints.categories import bp
from blueprints.decorators import get_params, variable, html_response, \
    entity_form, csrf_form, http_response
from persistence.model.category import Category
from persistence.repository.category import CategoryRepository
from security.decorators import has_role


@bp.route('/')
@get_params('search')
@variable('categories', CategoryRepository.find_all_by_name_like, 'search')
@variable('categories', CategoryRepository.find_all)
@html_response('categories/list.html', 'categories')
def list_all(categories):
    return categories


@bp.route('/view/<int:category_id>')
@variable('category', CategoryRepository.find_by_id, 'category_id')
@html_response('categories/view.html', 'category')
def view(category):
    return category


@bp.route('/create', methods=('GET', 'POST'))
@has_role('ADMIN')
@variable('category', Category)
@entity_form('form', 'category', csrf_validation=True, submit=True, repository=CategoryRepository)
@html_response('categories/form.html', 'form')
def create(form):
    if form.submitted_and_valid:
        flash('Category created.')

        return redirect(url_for('categories.list_all'))

    return form


@bp.route('/edit/<int:category_id>', methods=('GET', 'POST'))
@has_role('ADMIN')
@variable('category', CategoryRepository.find_by_id, 'category_id')
@entity_form('form', 'category', csrf_validation=True, submit=True, repository=CategoryRepository)
@html_response('categories/form.html', 'form')
def edit(form):
    if form.submitted_and_valid:
        flash('Category saved.')

        return redirect(url_for('categories.edit', category_id=form.entity.id))

    return form


@bp.route('/delete/<int:category_id>', methods=('POST',))
@has_role('ADMIN')
@variable('category', CategoryRepository.find_by_id, 'category_id')
@csrf_form('csrf', submit=True)
@http_response('category_id', 'csrf')
def delete(category_id, csrf):
    if csrf.errors:
        for error in csrf.errors:
            flash(error)
    else:
        try:
            CategoryRepository.delete_by_id(category_id)
            flash('Category deleted.')
        except Exception as err:
            flash(str(err))

    return redirect(url_for('categories.list_all'))
