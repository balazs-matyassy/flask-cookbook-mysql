from abc import ABC

from flask import request, session


class AbstractForm(ABC):
    def __init__(self, csrf_validation=False, json=False):
        self.csrf_validation = csrf_validation
        self.json = json
        self.submitted = False
        self.errors = []

    @property
    def submitted_and_valid(self):
        return self.submitted and len(self.errors) == 0

    def validate_on_submit(self):
        if request.method not in ('POST', 'PUT', 'DELETE'):
            return False
        elif not self.json and request.method != 'POST':
            return False

        self.submitted = True
        self.errors = []

        if request.is_json:
            if not self.json:
                self.errors.append('Form request expected.')
                return False
            elif self.csrf_validation and request.json.get('csrf_token') != session.get('csrf_token'):
                self.errors.append('Invalid CSRF token.')
                return False
        else:
            if self.json:
                self.errors.append('JSON request expected.')
            elif self.csrf_validation and request.form.get('csrf_token') != session.get('csrf_token'):
                self.errors.append('Invalid CSRF token.')
                return False

        return True
