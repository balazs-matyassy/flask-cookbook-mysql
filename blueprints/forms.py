from flask import request
from werkzeug.utils import secure_filename

from blueprints import AbstractForm
from persistence.mixins import FileMixin


class EntityForm(AbstractForm):
    def __init__(self, entity=None, fields=None, csrf_validation=False, json=False):
        super().__init__(csrf_validation, json)

        self.entity = entity
        self.fields = fields

    @property
    def create_form(self):
        return (self.entity is not None
                and self.entity.id is None)

    def validate_on_submit(self):
        if not super().validate_on_submit():
            return False

        if self.entity:
            form = request.form if not self.json else request.json

            if self.fields:
                form = {field: form[field] for field in self.fields}

            self.entity.form = form

            if isinstance(self.entity, FileMixin):
                file = request.files.get('file')

                if file and file.filename:
                    self.entity.filename = secure_filename(file.filename)
                    self.entity.mimetype = file.content_type
                    self.entity.content = file.stream.read()

            self.errors = self.entity.validate()

        return len(self.errors) == 0
