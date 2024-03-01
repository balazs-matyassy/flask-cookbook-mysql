from flask import request

from blueprints import AbstractForm


class LoginForm(AbstractForm):
    def __init__(self, username='', csrf_validation=False, json=False):
        super().__init__(csrf_validation, json)

        self.username = username
        self.password = ''

    def validate_on_submit(self):
        if not super().validate_on_submit():
            return False

        self.username = request.form.get('username', '').strip()
        self.password = request.form.get('password', '')

        if not self.username:
            self.errors.append('Username missing.')

        if not self.password:
            self.errors.append('Password missing.')

        return len(self.errors) == 0
