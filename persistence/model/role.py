from persistence.model import AbstractEntity


class Role(AbstractEntity):
    def __init__(self, role_id=None, **kwargs):
        super().__init__(**kwargs)

        self.id = role_id
        self.name = ''

        if kwargs:
            self.update(kwargs)

    @property
    def users(self):
        return UserRepository.find_all_by_role_id(self.id)

    @property
    def form(self):
        return {
            'id': self.id,
            'name': self.name
        }

    @form.setter
    def form(self, data):
        if 'name' in data:
            self.name = data['name'].strip().upper()

    def update(self, data):
        self.form = data

    def validate(self):
        errors = []

        if self.name == '':
            errors.append('Name missing.')

        return errors

    @staticmethod
    def create(data):
        if data is None:
            return None

        role = Role(role_id=data.get('id'))
        role.update(data)

        return role

    def __repr__(self):
        return f'<Role {self.name}>'


from persistence.repository.user import UserRepository
