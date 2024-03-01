from abc import abstractmethod


class AuthoringMixin:
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.created_at = None
        self.created_by = None
        self.modified_at = None
        self.modified_by = None

    @property
    def _authoring_form(self):
        return {
            'created_at': self.created_at,
            'created_by': self.created_by,
            'modified_at': self.modified_at,
            'modified_by': self.modified_by
        }

    def _update_authoring_data(self, data):
        if 'created_at' in data:
            self.created_at = data['created_at']

        if 'created_by' in data:
            self.created_by = data['created_by']

        if 'modified_at' in data:
            self.modified_at = data['modified_at']

        if 'modified_by' in data:
            self.modified_by = data['modified_by']


class OwnershipMixin:
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.owned_by = None

    @property
    def _ownership_form(self):
        return {
            'owned_by': self.owned_by
        }

    def _update_ownership_data(self, data):
        if 'owned_by' in data:
            self.owned_by = data['owned_by']


class FileMixin:
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.filename = None
        self.mimetype = None
        self.__content = None

    @property
    def basename(self):
        return self.filename.rsplit('.', 1)[0] if '.' in self.filename else self.filename

    @property
    def extension(self):
        return '' if '.' not in self.filename else self.filename.rsplit('.', 1)[1]

    @property
    def content(self):
        if not self.__content:
            self.__content = self._load_content()

        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    @property
    def _file_form(self):
        return {
            'filename': self.filename,
            'mimetype': self.mimetype,
            'content': self.content
        }

    @abstractmethod
    def _load_content(self):
        pass

    def _update_file_data(self, data):
        if 'filename' in data:
            self.filename = data['filename']

        if 'mimetype' in data:
            self.mimetype = data['mimetype']

        if 'content' in data:
            self.content = data['content']

    def _validate_file_data(self, allowed_extensions=None):
        errors = []

        if not self.filename:
            errors.append('Filename missing.')
        elif allowed_extensions and self.extension not in allowed_extensions:
            errors.append('Invalid file extension.')

        if not self.mimetype:
            errors.append('Mime type missing.')

        if not self.content:
            errors.append('Content missing.')

        return errors
