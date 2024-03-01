from werkzeug.security import generate_password_hash, check_password_hash

from persistence.mixins import AuthoringMixin
from persistence.model import AbstractEntity
from persistence.utils import try_parse_int


class User(AbstractEntity, AuthoringMixin):
    def __init__(self, user_id=None, **kwargs):
        super().__init__(**kwargs)

        self.id = user_id
        self.username = ''
        self.digest = None
        self.__role_id = None
        self.__role = None

        if kwargs:
            self.update(kwargs)

    @property
    def role_id(self):
        return self.__role_id

    @role_id.setter
    def role_id(self, value):
        self.__role_id = value
        self.__role = None

    @property
    def role(self):
        if self.__role:
            return self.__role

        return RoleRepository.find_by_id(self.__role_id)

    @role.setter
    def role(self, value):
        self.__role_id = value.id if value else None
        self.__role = value

    @property
    def password(self):
        return None

    @password.setter
    def password(self, value):
        if value:
            self.digest = generate_password_hash(value)

    @property
    def form(self):
        return {
            'id': self.id,
            'username': self.username,
            'digest': self.digest,
            'role_id': self.role_id,
            **self._authoring_form
        }

    @form.setter
    def form(self, data):
        if 'username' in data:
            self.username = data['username'].strip().lower()

        if 'password' in data:
            self.password = data['password']

        if 'role_id' in data:
            self.role_id = try_parse_int(data['role_id'])

    def check_password(self, password):
        return check_password_hash(self.digest, password)

    def update(self, data):
        self._update_authoring_data(data)

        if 'username' in data:
            self.username = data['username'].strip().lower()

        if 'digest' in data:
            self.digest = data['digest']

        if 'password' in data:
            self.password = data['password']

        if 'role_id' in data:
            self.role_id = data['role_id']

        if 'role' in data:
            self.role = data['role']

    def validate(self):
        errors = []

        if not self.username:
            errors.append('Username missing.')

        if not self.digest:
            errors.append('Password missing.')

        if not self.role_id:
            errors.append('Role missing.')
        elif not self.role:
            errors.append('Invalid role.')

        return errors

    @staticmethod
    def create(data):
        if data is None:
            return None

        user = User(user_id=data.get('id'))
        user.update(data)

        return user

    def __repr__(self):
        return f'<User {self.username}>'


from persistence.repository.role import RoleRepository
