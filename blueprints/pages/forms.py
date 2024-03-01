from flask import request

from blueprints import AbstractForm


class ChangePasswordForm(AbstractForm):
    def __init__(self, entity=None, csrf_validation=False, json=False):
        super().__init__(csrf_validation, json)

        self.entity = entity
        self.password = ''
        self.password_confirmation = ''

    def validate_on_submit(self):
        if not super().validate_on_submit():
            return False

        self.password = request.form.get('password', '')
        self.password_confirmation = request.form.get('password_confirmation', '')

        if not self.password:
            self.errors.append('Password missing.')

        if not self.password_confirmation:
            self.errors.append('Password confirmation missing.')

        if not self.errors and self.password != self.password_confirmation:
            self.errors.append('Password and password confirmation do not match.')

        if len(self.errors) == 0:
            self.entity.password = self.password

        return len(self.errors) == 0
