import secrets
import string
from urllib.parse import urlsplit

from flask import g, redirect, url_for, session, flash, request, render_template

from blueprints.security import bp
from blueprints.security.forms import LoginForm
from persistence.repository.user import UserRepository


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if g.user:
        return redirect(url_for('pages.home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = UserRepository.find_by_username(form.username)

        if user and user.check_password(form.password):
            session['user_id'] = user.id

            alphabet = string.ascii_letters + string.digits
            csrf_token = ''.join(secrets.choice(alphabet) for _ in range(32))
            session['csrf_token'] = csrf_token

            flash('Login successful.')

            if (request.args.get('redirect')
                    and not urlsplit(request.args.get('redirect')).netloc):
                return redirect(request.args.get('redirect'))

            return redirect(url_for('pages.home'))
        else:
            form.errors.append('Wrong username or password.')

    return render_template('security/login.html', form=form)


@bp.route('/logout')
def logout():
    session.clear()
    flash('Logout successful.')

    return redirect(url_for('pages.home'))
