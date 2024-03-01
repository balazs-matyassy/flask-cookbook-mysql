
from flask import flash, redirect, url_for

from blueprints.decorators import get_params, variable, html_response, entity_form, csrf_form, http_response
from blueprints.users import bp
from persistence.model.user import User
from persistence.repository.user import UserRepository
from security.decorators import has_role


@bp.route('/')
@has_role('ADMIN')
@get_params('search')
@variable('users', UserRepository.find_all_by_username_like, 'search')
@variable('users', UserRepository.find_all)
@html_response('users/list.html', 'users')
def list_all(users):
    return users


@bp.route('/create', methods=('GET', 'POST'))
@has_role('ADMIN')
@variable('user', User)
@entity_form('form', 'user', csrf_validation=True, submit=True, repository=UserRepository)
@html_response('users/form.html', 'form')
def create(form):
    if form.submitted_and_valid:
        flash('User created.')

        return redirect(url_for('users.list_all'))

    return form


@bp.route('/edit/<int:user_id>', methods=('GET', 'POST'))
@has_role('ADMIN')
@variable('user', UserRepository.find_by_id, 'user_id')
@entity_form('form', 'user', csrf_validation=True, submit=True, repository=UserRepository)
@html_response('users/form.html', 'form')
def edit(form):
    if form.submitted_and_valid:
        flash('User saved.')

        return redirect(url_for('users.edit', user_id=form.entity.id))

    return form


@bp.route('/delete/<int:user_id>', methods=('POST',))
@has_role('ADMIN')
@variable('user', UserRepository.find_by_id, 'user_id')
@csrf_form('csrf', submit=True)
@http_response('user_id', 'csrf')
def delete(user_id, csrf):
    if csrf.errors:
        for error in csrf.errors:
            flash(error)
    else:
        try:
            UserRepository.delete_by_id(user_id)
            flash('User deleted.')
        except Exception as err:
            flash(str(err))

    return redirect(url_for('users.list_all'))
